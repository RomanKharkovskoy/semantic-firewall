#!/usr/bin/env python3
"""Generate reproducible synthetic Semantic Firewall examples (stdlib only)."""
from __future__ import annotations

import ast
import csv
from dataclasses import dataclass
import difflib
import importlib.util
import json
from pathlib import Path
import random
import shutil
import sys

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
RNG = random.Random(20261114)

# Each case list is sampled in order into three non-overlapping scenario groups.
# These are semantic changes to business values; response schemas/signatures remain stable.
@dataclass(frozen=True)
class Mutation:
    family: str
    category: str
    provider: str
    method: str
    field: str
    kind: str  # number, bool, text
    old: str
    new: str
    cases: list[dict]
    notes: str


def m(family, category, provider, method, field, kind, old, new, cases, notes):
    if len(cases) != 9:
        raise ValueError(f"{family}: expected 9 inputs, got {len(cases)}")
    return Mutation(family, category, provider, method, field, kind, old, new, cases, notes)


def cases(keys, rows):
    return [dict(zip(keys.split(), row)) for row in rows]


MUTATIONS = [
    # PricingService: total includes VAT instead of net price, different coupon semantics, rounding mode.
    m('price_tax_inclusion','value_semantics','PricingService','quote','total','number',
      'result = round(float(request["subtotal"]), 2)',
      'result = round(float(request["subtotal"]) * (1 + float(request["vat_rate"])), 2)',
      cases('subtotal vat_rate',[(100,0.20),(50,0.10),(25,0),(120,0.20),(125,0.12),(5,0),(300,0.05),(19.99,0.20),(15,0.15)]),
      'Net amount becomes tax-inclusive while total remains numeric.'),
    m('coupon_tax_base','calculation_order','PricingService','quote','total','number',
      'result = round((float(request["subtotal"]) - float(request["coupon"])) * (1 + float(request["vat_rate"])), 2)',
      'result = round(float(request["subtotal"]) * (1 + float(request["vat_rate"])) - float(request["coupon"]), 2)',
      cases('subtotal coupon vat_rate',[(100,10,.2),(50,0,.2),(80,20,.1),(200,25,.12),(90,5,0),(30,6,.2),(500,50,.2),(40,0,.15),(75,15,.1)]),
      'Coupon stops reducing the taxable base.'),
    m('invoice_rounding','rounding','PricingService','quote','total','number',
      'result = float(Decimal(str(request["amount"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))',
      'result = float(Decimal(str(request["amount"])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))',
      cases('amount',[(10.125,),(10.135,),(10.12,),(12.345,),(12.355,),(12.34,),(20.005,),(100.015,),(5.2,)]),
      'Half-even monetary rounding changes to half-up.'),
    # ShippingService.
    m('free_shipping_limit','boundary_condition','ShippingService','estimate','fee','number',
      'result = 0.0 if float(request["cart_total"]) >= float(request["limit"]) else float(request["base_fee"])',
      'result = 0.0 if float(request["cart_total"]) > float(request["limit"]) else float(request["base_fee"])',
      cases('cart_total limit base_fee',[(100,100,12),(99,100,12),(110,100,12),(200,200,18),(250,200,18),(180,200,18),(500,500,25),(501,500,25),(490,500,25)]),
      'Free-shipping threshold changes from inclusive to exclusive.'),
    m('weight_unit_switch','unit_conversion','ShippingService','estimate','fee','number',
      'result = round(float(request["weight_g"]) / 1000 * float(request["price_per_kg"]), 2)',
      'result = round(float(request["weight_g"]) * float(request["price_per_kg"]), 2)',
      cases('weight_g price_per_kg',[(1000,15),(250,12),(0,15),(700,10),(1400,8),(0,20),(125,20),(2500,10),(5,10)]),
      'Weight input is silently treated as kilograms rather than grams.'),
    m('remote_shipping_fee','fallback_policy','ShippingService','estimate','fee','number',
      'result = round(float(request["base_fee"]) + (float(request["remote_fee"]) if request["is_remote"] else 0.0), 2)',
      'result = round(float(request["base_fee"]), 2)',
      cases('base_fee remote_fee is_remote',[(15,20,True),(15,20,False),(0,15,True),(12,10,False),(9,30,True),(12,0,True),(40,25,True),(20,25,False),(8,9,True)]),
      'Remote-area surcharge stops being added.'),
    # InventoryService.
    m('reserved_stock','value_semantics','InventoryService','availability','available','number',
      'result = max(0, int(request["on_hand"]) - int(request["reserved"]))',
      'result = max(0, int(request["on_hand"]))',
      cases('on_hand reserved',[(10,3),(5,0),(0,0),(12,8),(6,6),(0,2),(100,35),(9,1),(2,0)]),
      'Available stock stops subtracting outstanding reservations.'),
    m('backorder_policy','fallback_policy','InventoryService','availability','available','bool',
      'result = int(request["on_hand"]) >= int(request["requested"])',
      'result = int(request["on_hand"]) + int(request["incoming"]) >= int(request["requested"])',
      cases('on_hand incoming requested',[(3,5,6),(3,1,3),(0,0,1),(4,3,7),(4,1,8),(10,0,7),(0,9,8),(2,2,4),(7,0,7)]),
      'Incoming stock begins counting as available before receipt.'),
    m('warehouse_selection','ordering','InventoryService','route','warehouse_id','text',
      'result = min(request["warehouses"], key=lambda w: (w["distance_km"], w["id"]))["id"]',
      'result = max(request["warehouses"], key=lambda w: (w["stock"], w["id"]))["id"]',
      [
        {'warehouses':[{'id':'W1','distance_km':5,'stock':1},{'id':'W2','distance_km':18,'stock':30}]},
        {'warehouses':[{'id':'W3','distance_km':7,'stock':9},{'id':'W4','distance_km':9,'stock':1}]},
        {'warehouses':[{'id':'W5','distance_km':2,'stock':7},{'id':'W6','distance_km':12,'stock':10}]},
        {'warehouses':[{'id':'W7','distance_km':1,'stock':2},{'id':'W8','distance_km':10,'stock':20}]},
        {'warehouses':[{'id':'W9','distance_km':2,'stock':40},{'id':'W0','distance_km':20,'stock':1}]},
        {'warehouses':[{'id':'WA','distance_km':3,'stock':4},{'id':'WB','distance_km':4,'stock':5}]},
        {'warehouses':[{'id':'WC','distance_km':8,'stock':1},{'id':'WD','distance_km':15,'stock':12}]},
        {'warehouses':[{'id':'WE','distance_km':3,'stock':90},{'id':'WF','distance_km':30,'stock':1}]},
        {'warehouses':[{'id':'WG','distance_km':4,'stock':10},{'id':'WH','distance_km':4,'stock':15}]},
      ],'Nearest warehouse is replaced with highest-stock warehouse.'),
    # OrderService.
    m('order_status_name','enum_semantics','OrderService','summary','status','text',
      'result = "PAID" if request["captured"] else "PENDING"',
      'result = "COMPLETE" if request["captured"] else "PENDING"',
      cases('captured',[(True,),(False,),(True,),(True,),(False,),(False,),(True,),(True,),(False,)]),
      'Paid order status string changes without changing its field type.'),
    m('cancel_window','boundary_condition','OrderService','cancellable','allowed','bool',
      'result = float(request["hours_since_order"]) <= 24',
      'result = float(request["hours_since_order"]) < 24',
      cases('hours_since_order',[(24,),(23,),(25,),(24,),(12,),(24.1,),(24,),(0,),(23.99,)]),
      'Cancellation deadline becomes exclusive.'),
    m('retry_idempotency','idempotency','OrderService','create','order_id','number',
      'result = int(request["existing_id"]) if request["is_retry"] else int(request["existing_id"]) + 1',
      'result = int(request["existing_id"]) + 1',
      cases('existing_id is_retry',[(100,True),(101,False),(102,True),(200,False),(205,True),(210,False),(300,True),(305,True),(310,False)]),
      'Retry starts issuing a new order identifier.'),
    # LoyaltyService.
    m('vip_tier_limit','boundary_condition','LoyaltyService','tier','tier','text',
      'result = "VIP" if int(request["points"]) >= int(request["threshold"]) else "STANDARD"',
      'result = "VIP" if int(request["points"]) > int(request["threshold"]) else "STANDARD"',
      cases('points threshold',[(1000,1000),(999,1000),(1001,1000),(200,200),(210,200),(190,200),(5000,5000),(4999,5000),(6000,5000)]),
      'Loyalty tier changes at the exact threshold.'),
    m('points_per_amount','unit_conversion','LoyaltyService','earn','points','number',
      'result = int(float(request["spent"]) // 10)',
      'result = int(float(request["spent"]) // 5)',
      cases('spent',[(100,),(5,),(0,),(50,),(9,),(20,),(75,),(40,),(1,)]),
      'Earning rate doubles with unchanged integer points schema.'),
    m('reward_expiration','boundary_condition','LoyaltyService','validity','valid','bool',
      'result = int(request["days_old"]) <= 30',
      'result = int(request["days_old"]) <= 14',
      cases('days_old',[(20,),(10,),(31,),(14,),(25,),(0,),(30,),(35,),(16,)]),
      'Points expire after fourteen days instead of thirty.'),
    # CatalogService.
    m('sku_case_policy','normalization','CatalogService','normalize','sku','text',
      'result = str(request["sku"]).strip().upper()',
      'result = str(request["sku"]).strip().lower()',
      cases('sku',[(' Ab-12 ',),('z9',),('  ',),('B-CD',),('Q10',),(' x-y ',),('prod-123',),('V2 ',),('AZ',)]),
      'SKU canonicalization switches case.'),
    m('out_of_stock_display','fallback_policy','CatalogService','visibility','visible','bool',
      'result = int(request["stock"]) > 0',
      'result = int(request["stock"]) > 0 or bool(request["allow_backorder"])',
      cases('stock allow_backorder',[(0,True),(1,True),(0,False),(0,True),(2,False),(0,False),(0,True),(4,True),(0,False)]),
      'Out-of-stock products become visible when backorders are allowed.'),
    m('catalog_rank','ordering','CatalogService','top_item','sku','text',
      'result = sorted(request["items"], key=lambda item: (-item["score"], item["sku"]))[0]["sku"]',
      'result = sorted(request["items"], key=lambda item: (item["title"], item["sku"]))[0]["sku"]',
      [
        {'items':[{'sku':'K1','title':'Zebra','score':8},{'sku':'K2','title':'Apple','score':4}]},
        {'items':[{'sku':'K3','title':'Apple','score':9},{'sku':'K4','title':'Berry','score':5}]},
        {'items':[{'sku':'K5','title':'Yacht','score':7},{'sku':'K6','title':'Alto','score':2}]},
        {'items':[{'sku':'L1','title':'Omega','score':8},{'sku':'L2','title':'Alfa','score':10}]},
        {'items':[{'sku':'L3','title':'Alfa','score':5},{'sku':'L4','title':'Beta','score':9}]},
        {'items':[{'sku':'L5','title':'Cyan','score':4},{'sku':'L6','title':'Amber','score':1}]},
        {'items':[{'sku':'M1','title':'Silver','score':8},{'sku':'M2','title':'Bronze','score':2}]},
        {'items':[{'sku':'M3','title':'Amber','score':3},{'sku':'M4','title':'Tango','score':9}]},
        {'items':[{'sku':'M5','title':'Banana','score':9},{'sku':'M6','title':'Apple','score':8}]},
      ],'Top item changes from relevance score to title order.'),
    # BillingService.
    m('processing_fee_cap','boundary_condition','BillingService','calculate','fee','number',
      'result = round(min(float(request["amount"]) * float(request["rate"]), float(request["cap"])), 2)',
      'result = round(float(request["amount"]) * float(request["rate"]), 2)',
      cases('amount rate cap',[(1000,.1,50),(100,.1,50),(500,.15,60),(200,.2,20),(100,.05,30),(500,.1,80),(2000,.06,80),(50,.1,10),(1000,.2,100)]),
      'Processing fee stops respecting its maximum cap.'),
    m('invoice_due_days','temporal_semantics','BillingService','deadline','due_date','text',
      'result = (date.fromisoformat(request["issued_on"]) + timedelta(days=30)).isoformat()',
      'result = (date.fromisoformat(request["issued_on"]) + timedelta(days=14)).isoformat()',
      cases('issued_on',[('2026-01-15',),('2026-02-28',),('2026-03-01',),('2026-04-04',),('2026-06-30',),('2026-07-07',),('2026-08-08',),('2026-11-10',),('2026-12-31',)]),
      'Invoice due date is moved sixteen days earlier.'),
    m('refund_includes_delivery','value_semantics','BillingService','refund','refund','number',
      'result = round(float(request["item_amount"]), 2)',
      'result = round(float(request["item_amount"]) + float(request["delivery_fee"]), 2)',
      cases('item_amount delivery_fee',[(80,10),(50,0),(120,15),(99,5),(20,0),(60,12),(200,30),(30,0),(10,2)]),
      'Refund changes from items-only to items plus delivery.'),
    # NotificationService.
    m('locale_default','fallback_policy','NotificationService','language','locale','text',
      'result = request.get("locale") or "ru"',
      'result = request.get("locale") or "en"',
      cases('locale',[(None,),('ru',),('en',),(None,),('fr',),('ru',),(None,),('de',),('',)]),
      'Missing locale now defaults to English instead of Russian.'),
    m('notification_retry','idempotency','NotificationService','dispatch','should_send','bool',
      'result = not bool(request["already_sent"])',
      'result = True',
      cases('already_sent',[(True,),(False,),(True,),(False,),(True,),(False,),(True,),(False,),(True,)]),
      'Repeated notifications are sent again.'),
    m('incident_priority','enum_semantics','NotificationService','priority','priority','text',
      'result = "urgent" if request["severity"] == "high" else "normal"',
      'result = "normal"',
      cases('severity',[('high',),('low',),('medium',),('high',),('low',),('high',),('medium',),('high',),('low',)]),
      'High-severity events lose their urgent priority.'),
    # PaymentService.
    m('payment_fee_basis','calculation_order','PaymentService','settle','net_amount','number',
      'result = round(float(request["gross"]) - float(request["fixed_fee"]) - float(request["gross"]) * float(request["rate"]), 2)',
      'result = round((float(request["gross"]) - float(request["fixed_fee"])) * (1 - float(request["rate"])), 2)',
      cases('gross fixed_fee rate',[(100,10,.2),(100,0,.2),(50,5,.1),(200,20,.15),(150,10,0),(40,5,.2),(90,10,.1),(30,0,.15),(1000,100,.05)]),
      'Percent payment fee is charged on a different base.'),
    m('duplicate_capture','idempotency','PaymentService','capture','captured_amount','number',
      'result = 0.0 if request["was_captured"] else float(request["amount"])',
      'result = float(request["amount"])',
      cases('amount was_captured',[(100,True),(100,False),(0,True),(50,True),(40,False),(30,True),(200,True),(200,False),(20,True)]),
      'Repeated capture unexpectedly charges the full amount.'),
    m('payment_minor_units','unit_conversion','PaymentService','capture','captured_amount','number',
      'result = round(float(request["amount_minor"]) / 100, 2)',
      'result = round(float(request["amount_minor"]), 2)',
      cases('amount_minor',[(1050,),(0,),(99,),(2500,),(10000,),(1,),(750,),(150,),(0,)]),
      'Minor currency units are silently treated as major units.'),
]

SERVICE_CONSUMERS = {
    'PricingService':['CheckoutService','ReceiptService','OrderService','FinanceService','SalesAnalyticsService','CustomerPortalService'],
    'ShippingService':['CheckoutService','FulfillmentService','ReturnsService','TrackingService','CustomerPortalService','SalesAnalyticsService'],
    'InventoryService':['CheckoutService','FulfillmentService','WarehouseService','ProcurementService','StorefrontService','SalesAnalyticsService'],
    'OrderService':['BillingService','FulfillmentService','CustomerPortalService','SupportService','SalesAnalyticsService','NotificationService'],
    'LoyaltyService':['CheckoutService','RewardsService','CustomerPortalService','CRMService','MarketingService','SalesAnalyticsService'],
    'CatalogService':['StorefrontService','SearchService','CheckoutService','RecommendationsService','MarketingService','SalesAnalyticsService'],
    'BillingService':['FinanceService','CheckoutService','CollectionsService','CustomerPortalService','SalesAnalyticsService','SupportService'],
    'NotificationService':['CustomerPortalService','SupportService','MarketingService','AuditService','CRMService','SalesAnalyticsService'],
    'PaymentService':['CheckoutService','FinanceService','FraudService','BillingService','SupportService','SalesAnalyticsService'],
}


def provider_source(mutation, version, variant):
    expr = mutation.old if version == 'old' else mutation.new
    output=f'return {{{mutation.field!r}: result, "request_id": request["request_id"]}}'
    if variant == 0:
        lines=[f'def {mutation.method}(request: dict) -> dict:',
               *['    '+x for x in expr.splitlines()],
               '    '+output,'']
    elif variant == 1:
        # Refactoring-style change: the public endpoint delegates to a private helper.
        lines=['def _calculate(request: dict):',
               *['    '+x for x in expr.splitlines()],
               '    return result','',
               f'def {mutation.method}(request: dict) -> dict:',
               '    result = _calculate(request)',
               '    '+output,'']
    elif variant == 2:
        # A nested function carries the business rule and depends on the call context.
        lines=[f'def {mutation.method}(request: dict) -> dict:',
               '    def compute():',
               *['        '+x for x in expr.splitlines()],
               '        return result',
               '    result = compute()',
               '    '+output,'']
    else:
        raise ValueError(variant)
    imports = ''
    if 'Decimal(' in expr:
        rounding = 'ROUND_HALF_EVEN' if 'ROUND_HALF_EVEN' in expr else 'ROUND_HALF_UP'
        imports = f'from decimal import Decimal, {rounding}\n\n'
    elif 'date.fromisoformat' in expr:
        imports = 'from datetime import date, timedelta\n\n'
    return imports+'\n'.join(lines)


def consumer_source(mutation, role, boundary, bucket):
    field=mutation.field; method=mutation.method
    first=f'def process(provider, request: dict) -> dict:\n    response = provider.{method}(request)\n'
    if role=='direct':
        tail=f'    return {{"observed": response[{field!r}], "reference": response["request_id"]}}\n'
    elif role=='metadata':
        tail='    return {"audit_reference": response["request_id"]}\n'
    elif role=='resilient':
        if mutation.kind=='number':
            tail=f'    return {{"any_amount": float(response[{field!r}]) > 0}}\n'
        elif mutation.kind=='bool':
            tail=f'    return {{"continue": bool(response[{field!r}]) or request.get("audit_enabled", False)}}\n'
        else:
            tail=f'    return {{"route_prefix": str(response[{field!r}]).casefold()[:1]}}\n'
    elif role=='guarded':
        fallback={'number': '0', 'bool':'False', 'text':'"not_requested"'}[mutation.kind]
        tail=f'    chosen = response[{field!r}] if request.get("use_result", False) else {fallback}\n    return {{"selected": chosen}}\n'
    elif role=='derived':
        if mutation.kind=='number':
            tail=f'    return {{"policy_triggered": float(response[{field!r}]) >= {boundary!r}}}\n'
        elif mutation.kind=='bool':
            tail=f'    return {{"outcome": "allowed" if response[{field!r}] else "blocked"}}\n'
        else:
            tail=f'    return {{"routing_key": str(response[{field!r}])[:2]}}\n'
    elif role=='normalized':
        if mutation.kind=='number':
            tail=f'    return {{"report_bucket": int(float(response[{field!r}]) // {bucket!r})}}\n'
        elif mutation.kind=='bool':
            tail=f'    return {{"audit_flag": bool(response[{field!r}]) and request.get("audit_enabled", False)}}\n'
        else:
            tail=f'    return {{"normalized_value": str(response[{field!r}]).casefold()}}\n'
    else:
        raise ValueError(role)
    return first+tail


def load_source(name, path):
    spec=importlib.util.spec_from_file_location(name,str(path))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_consumer(source, provider, request, name):
    namespace={}
    exec(compile(source,name,'exec'),namespace)
    # No dangerous inputs: all source from our fixed templates and static fixture specs.
    return namespace['process'](provider,request)


def value_of(mutation, module, request):
    return getattr(module,mutation.method)(request)[mutation.field]


def stable_json(obj):
    return json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'))


def generate():
    raw=ROOT/'data'/'raw'/'scenarios'
    audit=ROOT/'data'/'audit'
    for path in (raw, audit/'contracts'):
        if path.exists(): shutil.rmtree(path)
    raw.mkdir(parents=True,exist_ok=True)
    processed=ROOT/'data'/'processed'; processed.mkdir(parents=True,exist_ok=True)
    audit.mkdir(parents=True,exist_ok=True)
    records=[]; audits=[]; scenarios=[]; graph=set()
    family_ids=[m.family for m in MUTATIONS]
    assert len(family_ids)==len(set(family_ids))
    # Entire mutation family is kept in one split, avoiding near-identical variants crossing folds.
    shuffled=family_ids.copy(); RNG.shuffle(shuffled)
    split_by_family={fam:('train' if i<19 else 'validation' if i<23 else 'test') for i,fam in enumerate(shuffled)}
    for mutation in MUTATIONS:
        for variant in range(3):
            scenario_id=f'{mutation.family}_v{variant+1:02d}'
            base=raw/scenario_id
            (base/'consumers').mkdir(parents=True,exist_ok=True)
            (audit/'contracts'/scenario_id).mkdir(parents=True,exist_ok=True)
            old_path=base/'provider_old.py';new_path=base/'provider_new.py'
            old_source=provider_source(mutation,'old',variant);new_source=provider_source(mutation,'new',variant)
            assert ast.dump(ast.parse(old_source),include_attributes=False)!=ast.dump(ast.parse(new_source),include_attributes=False)
            old_path.write_text(old_source,encoding='utf-8');new_path.write_text(new_source,encoding='utf-8')
            old_mod=load_source(f'old_{scenario_id}',old_path)
            new_mod=load_source(f'new_{scenario_id}',new_path)
            diff_path=base/'change.diff'
            diff=''.join(difflib.unified_diff(old_source.splitlines(keepends=True),new_source.splitlines(keepends=True),fromfile=f'a/{mutation.provider.lower()}.py',tofile=f'b/{mutation.provider.lower()}.py'))
            assert diff.startswith('--- a/') and '@@' in diff
            diff_path.write_text(diff,encoding='utf-8')
            selected=mutation.cases[variant*3:(variant+1)*3]
            request_cases=[]
            for idx,r in enumerate(selected):
                d={**r,'request_id':f'TRX-{variant+1:02d}{idx+1:02d}-{mutation.provider[:3].upper()}'}
                # Purely exogenous optional flags, independent of label.
                d['use_result'] = (idx+variant) % 3 != 1
                d['audit_enabled'] = (idx+variant) % 3 != 2
                request_cases.append(d)
            # Field names and JSON types must be preserved for every request.
            schema=lambda resp: {k:type(v).__name__ for k,v in resp.items()}
            old_out=[getattr(old_mod,mutation.method)(req) for req in request_cases]
            new_out=[getattr(new_mod,mutation.method)(req) for req in request_cases]
            for o,n in zip(old_out,new_out):
                assert schema(o)==schema(n), (scenario_id,o,n)
                assert o.keys()==n.keys()
            old_values=[x[mutation.field] for x in old_out]
            # Threshold derived from old behavior ONLY (not from mutated code or labels).
            if mutation.kind=='number':
                baseline=float(old_values[0]); magnitude=max(abs(baseline),1.)
                boundary=round(baseline if abs(baseline)<100 else baseline*0.85,2)
                bucket=max(1,round(magnitude/5))
            else:
                boundary=1; bucket=10
            roles=['direct','derived','normalized','guarded','metadata' if variant==0 else 'resilient']
            consumers=RNG.sample(SERVICE_CONSUMERS[mutation.provider],k=5)
            RNG.shuffle(roles)
            changed_behavior=any(x!=y for x,y in zip(old_values,[x[mutation.field] for x in new_out]))
            for role,consumer in zip(roles,consumers):
                consumer_file=base/'consumers'/f'{consumer}.py'
                code=consumer_source(mutation,role,boundary,bucket)
                consumer_file.write_text(code,encoding='utf-8')
                expected=[run_consumer(code,old_mod,req,f'{scenario_id}:{consumer}') for req in request_cases]
                actual=[run_consumer(code,new_mod,req,f'{scenario_id}:{consumer}') for req in request_cases]
                old_pass=True
                new_pass=all(x==y for x,y in zip(expected,actual))
                label=0 if new_pass else 1
                contract={'contract_schema_version':1,'scenario_id':scenario_id,'consumer':consumer,
                          'requests':request_cases,'expected_from_old_provider':expected}
                contract_path=audit/'contracts'/scenario_id/f'{consumer}.json'
                contract_path.write_text(json.dumps(contract,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
                pair_id=f'pair_{len(records)+1:04d}'
                lines_added=sum(1 for line in diff.splitlines() if line.startswith('+') and not line.startswith('+++'))
                lines_deleted=sum(1 for line in diff.splitlines() if line.startswith('-') and not line.startswith('---'))
                records.append({
                  'pair_id':pair_id,'scenario_id':scenario_id,'family_id':mutation.family,'split':split_by_family[mutation.family],
                  'provider':mutation.provider,'consumer':consumer,'change_type':mutation.category,
                  'diff_path':diff_path.relative_to(ROOT).as_posix(),
                  'provider_old_path':old_path.relative_to(ROOT).as_posix(),
                  'provider_new_path':new_path.relative_to(ROOT).as_posix(),
                  'consumer_code_path':consumer_file.relative_to(ROOT).as_posix(),
                  'num_files_changed':1,'lines_added':lines_added,'lines_deleted':lines_deleted,
                  'diff_chars':len(diff),'consumer_code_chars':len(code),
                  'api_schema_unchanged':1,'label':label,
                })
                audits.append({'pair_id':pair_id,'contract_path':contract_path.relative_to(ROOT).as_posix(),
                   'old_tests_pass':int(old_pass),'new_tests_pass':int(new_pass),'checked_cases':len(request_cases),
                   'observed_breaking':label,'provider_output_changed':int(changed_behavior)})
                graph.add((mutation.provider,consumer))
            scenarios.append({'scenario_id':scenario_id,'family_id':mutation.family,'change_type':mutation.category,'provider':mutation.provider,
                'method':mutation.method,'field':mutation.field,'output_kind':mutation.kind,
                'split':split_by_family[mutation.family],'business_change':mutation.notes,
                'provider_output_changed_for_test_cases':int(changed_behavior),
                'num_consumers':len(consumers),'num_contract_cases':len(request_cases)})
    def write_csv(path,rows):
        with path.open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
            writer.writeheader();writer.writerows(rows)
    write_csv(processed/'pairs.csv',records)
    write_csv(processed/'scenarios.csv',scenarios)
    write_csv(audit/'label_audit.csv',audits)
    edges=[{'provider':p,'consumer':c} for p,c in sorted(graph)]
    write_csv(processed/'dependency_edges.csv',edges)
    manifest={'dataset_name':'Semantic Firewall synthetic semantic-compatibility fixtures','dataset_version':'1.0.0',
        'seed':20261114,'entirely_synthetic':True,'language':'Python','dataset_unit':'(code change, consumer service)',
        'labeling_rule':'Unchanged consumer contract snapshots: old provider passes, new provider fail => 1; both pass => 0',
        'label_note':'0 means compatible only within the three supplied contract cases, not universally compatible',
        'test_oracle':'Golden outputs captured under old provider for unchanged consumers; self-consistent, not externally validated',
        'no_real_network_calls':True,'repository_alignment':'docs/ml_system_design_doc.md on hw_1',
        'pairs':len(records),'changes':len(scenarios),'families':len(MUTATIONS),'provider_services':len(SERVICE_CONSUMERS),
        'frozen_split_level':'family_id','split_counts':{name:sum(r['split']==name for r in records) for name in ('train','validation','test')},
        'excluded_from_model_features':['label','split','pair_id','scenario_id','family_id','label_audit.csv',
                                        'contract JSON expected_from_old_provider','old_tests_pass','new_tests_pass',
                                        'observed_breaking','provider_output_changed','business_change'],
        'schema_guarantee':'Python call signature, response keys, and response value types stay unchanged within each scenario'}
    (ROOT/'data'/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'pairs':len(records),'scenarios':len(scenarios),'families':len(MUTATIONS),
         'labels':{i:sum(x['label']==i for x in records) for i in (0,1)},
         'unchanged_behavior_scenarios':sum(not s['provider_output_changed_for_test_cases'] for s in scenarios),
         'categories':len({x.category for x in MUTATIONS})},indent=2))

if __name__=='__main__':
    generate()
