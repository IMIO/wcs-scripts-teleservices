# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Commune(town.Town):

    def __init__(self):
        super(Commune, self).__init__(variables=globals())

    def test(self, test):
        if test == 'essais':
            return True
        else:
            return False

    def get_roles(self, *args):
        user = globals().get("session_user")
        form = globals().get("form_objects")._formdef
        for q in user.get_roles():
            if q in form.roles:
                return True
        return False

    # Pratique pour prendre le raw d'un champs date et pour récupérer une string formattée comme on veut.
current_commune = Commune()
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
