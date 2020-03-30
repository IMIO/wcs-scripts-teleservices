# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')

def how_many_encoded_diseases(context):
    if context.get('form_var_maladies') is None:
        diseases = []
    if context.get('form_var_autres_maladies') is None:
        other_diseases = []

    result = len(diseases) + len(other_diseases)
    
    return result

result = how_many_encoded_diseases(vars())
