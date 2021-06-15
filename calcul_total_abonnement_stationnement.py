# -*- coding: utf8 -*-

def calcul_prix(context):
    data = context.get('form_var_donnees_vignettes_raw_data')
    total = None
    if data:
        total = 0
        for price_list in data:
            price = price_list['bfd879368c-94ae-4f33-884d-873129b1076b_structured']
            price = int(price['price'])
            total += price
    return total


result = calcul_prix(vars())
