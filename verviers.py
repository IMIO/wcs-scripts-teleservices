# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re
import ast
from decimal import Decimal 

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

def estim_loc_matos(data_source_materiel, intervention, demands):
    #data_sources_materiel is a data_sources which contains all materiel and prices with and without intervention
    #intervention is a boolean from the form.
    #demands is a dictionnary that contains, for each field, the name of the var and his value
    total = 0
    for item in data_source_materiel:
        if item['id'] in demands:
            price = item['unit_price_with_intervention'] if intervention in [True,'True','Oui'] else item['unit_price']
            total += Decimal(price or 0) * Decimal(demands[item['id']] or 0)
    return total


arguments = [argument for argument in args]
if arguments[0] == "estim_loc_matos":
    demands = ast.literal_eval(arguments[3])
    for key in demands.keys():
        demands[key] = vars().get(demands[key])
    result = str(estim_loc_matos(data_source.materiel, vars().get(arguments[2]), demands))
