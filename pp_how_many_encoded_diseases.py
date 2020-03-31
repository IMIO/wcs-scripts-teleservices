# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')

def how_many_encoded_diseases(context):
    return len(context.get('form_var_diseases_raw') or []) + len(context.get('form_var_other_diseases') or [])

result = how_many_encoded_diseases(vars())

