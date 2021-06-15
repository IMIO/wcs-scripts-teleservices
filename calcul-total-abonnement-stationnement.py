# -*- coding: utf8 -*-
prices = vars().get('form_var_donnees_vignettes_raw')

total = 0

prices_list = prices['data']

for price_list in prices_list:
    price = price_list['bfd879368c-94ae-4f33-884d-873129b1076b_structured']
    price = int(price['price'])
    total += price

result = total
