# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Verviers(town.Town):

    def __init__(self):
        super(Verviers, self).__init__(variables=globals())
        self.lst_motifs_dispo = globals().get('form_option_motifs_disponibles_structured')

    def helloworld(self, args):
        return 'hello'

    def estim_loc_matos (data_sources_materiel, intervention, **kwargs):
        #data_sources_materiel is a data_sources which contains all materiel and prices with and without intervention
        #intervention is a boolean from the form.
        #**kwargs contains, for each field, the name of the var and his value
        total = 0
        for item in data_sources_materiel:
            if item['id'] in kwargs:
                price = item['unit_price_with_intervention'] if intervention == 'True' else item['unit_price']
                total += Decimal(price or 0) * Decimal(kwargs[item['id']] or 0)
        return str('total')

current_commune = Verviers()
function = args[0]

functionList = {function: getattr(current_commune,function)}
if args[1] is not None:
    parameters = args[1]
    if isinstance(parameters, dict):
        result = functionList[function](**parameters)
    else:
        params = args[1:]
        result = functionList[function](*params)
else:
    result = functionList[function]()

