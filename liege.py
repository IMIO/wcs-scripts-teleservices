# -*- coding: utf-8 -*-
from decimal import Decimal
import sys
import re
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')

if 'town' in sys.modules:
    del sys.modules['town']

import town

liege_cities = set(['Ch\xc3\xaan\xc3\xa9e', 'angleur', 'Bressoux', 'Chênée', 'Glain', 'Grivegnée', 'Jupille','Jupille-sur-Meuse', 'Liège', 'Rocourt', 'Wandre'])


class Liege(town.Town):

    def __init__(self):
        super(Liege, self).__init__(variables=globals())

    def is_not_liege_filtered_list(self, choices, is_not_liege_filtered_list = [], forms_exceptions= []):
        if not self.user_zipcode:
            return choices
        if self.user_zipcode in ('4000', '4020', '4030', '4031', '4032'):
            return choices
        else:
            if self.form_slug in forms_exceptions:
                return choices
            else:
                return [x for i, x in enumerate(choices) if i in is_not_liege_filtered_list]

    def is_liege_resident(self, choices, is_liege_filtered_list = [], is_not_liege_filtered_list = [], is_authentication_aware = 'False'):
        if not self.user_zipcode or (self.user_birthplace is None  and is_authentication_aware == 'True'):
            return choices
        if self.user_zipcode in ('4000', '4020', '4030', '4031', '4032'):
            if ((self.user_birthplace is None or self.user_birthplace == '') and is_authentication_aware == 'True'):
                return choices
            else:
                if len(is_liege_filtered_list) > 0:
                    return [x for i, x in enumerate(choices) if i in is_liege_filtered_list]
                else:
                    return choices
        else:
            if len(is_not_liege_filtered_list) > 0:
                return [x for i, x in enumerate(choices) if i in is_not_liege_filtered_list]
            else:
                return choices

    def verif_liege_wedding(self, wedding_cities):
        if wedding_cities in liege_cities or wedding_cities is None:
            return True
        else:
            return False

    def had_liege_wedding(self, choices, is_not_liege_filtered_list = []):
        # BAEC Hack
        if self.user_wedding_cities != '':
            return choices
        else:
            return [x for i, x in enumerate(choices) if i in is_not_liege_filtered_list]
        #if not self.user_wedding_cities:
        #    return choices
        #if liege_cities.intersection(self.user_wedding_cities.split('|')):
        #    return choices
        #else:
        #    return [x for i, x in enumerate(choices) if i in is_not_liege_filtered_list]

    def has_liege_birthplace(self, choices, is_not_liege_filtered_list = []):
        # BAEC Hack
        return choices
        #if not self.user_birthplace:
        #    return choices
        #if self.user_birthplace in liege_cities:
        #    return choices
        #else:
        #    return [x for i, x in enumerate(choices) if i in is_not_liege_filtered_list]


    def test_liege_and_return_text(self, is_liege_text, is_not_liege_text):
        if self.user_zipcode  in ('4000', '4020', '4030', '4031', '4032'):
            return is_liege_text
        else:
            return is_not_liege_text

    # This is a very specific function to validate a dynamic table in a specific form for LIEGE
    # This form is "Commande courrier/fax/mail"
    def validate_specific_computing_tab(self, table_var, lst_cols1, lst_cols2):
        retour = True
        try:
            for item in table_var:
                index_elems_to_convert = lst_cols1 + lst_cols2
                i = 0
                new_list = []
                while i < len(item):
                    value = item[i]
                    if i in index_elems_to_convert:
                        if value == '':
                            value = value.replace("","0")
                        value = int(value)
                    new_list.append(value)
                    i = i + 1
                sum_cols1_values = sum([new_list[index] for index in lst_cols1])
                sum_cols2_values = sum([new_list[index] for index in lst_cols2])
                if sum_cols1_values != sum_cols2_values:
                    retour = False
            return retour
        except:
            return False

    def simplified_belgium_iban_validator(self, iban_number):
        result = False
        key = iban_number[2:4]
        if len(iban_number) == 16:
            if iban_number[0:2] == "BE":
                B = "11"
                E = "14"
                if re.match("^[0-9]*$", iban_number[2:16]):
                    valid_key = 98 - (int(iban_number[4:16] + B + E + "00") % 97)
                    if int(key) == valid_key:
                        tmp_iban_number = iban_number[4:16] + B + E + iban_number[2:4]
                        if int(tmp_iban_number) % 97 == 1:
                            result = True
        return result

    def conteneurs_verts(self, datasource, auth=None, ws=None):
        if len(ws) <= 1:
           for item in datasource[1:]:
                item['disabled'] = True
        else:
            datasource[0]['disabled'] = True
        return datasource

    def vignette_table_compute(self, table_var, id_colonne, datasource):
        result = "0"
        id_col = int(id_colonne)
        if table_var is not None:
            for item in table_var:
                for vignette in datasource:
                    if vignette['id'] == item[id_col]:
                        item[id_col] = vignette['price']
            result = self.compute_dynamic_tab(table_var, id_colonne)
        return result

    def vignette_total(self, *args):
        table_var = globals().get(args[0])
        id_colonne = args[1]
        datasource = args[2]
        total = str(Decimal(globals().get('form_var_vignette_price') or 0) 
                if (globals().get('form_var_nombre') == "une nouvelle vignette de stationnement") 
                else 
                    Decimal(self.vignette_table_compute(table_var, id_colonne, datasource)))
        return total

    #Cette méthode à pour mission d'enrichir la liste des vignettes commandée par l'usager avec leurs
    #dates de validité. Pour ce faire, elle compare l'id de la variable du formulaire à une datasource
    #qui contient les données manquantes.
    def vignettes(self, form_var_tab_vignettes, dts):
    #dts désigne "DaTaSource". Cette datasource contient entre autre les dates de début et de fin
    #de validité des vignettes
        new_list = []
        for item in form_var_tab_vignettes:
            for dic in dts:
                if item[3] == dic.get('id'):
                    new_list.append(item)
                    new_list[-1].append(dic.get('start_date'))
                    new_list[-1].append(dic.get('end_date'))
        return new_list

    def test(self, a):
        return type(Town)


    def test(self, a):
        return type(Town)

current_commune = Liege()
# args[0] is the function name calling in WCS
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
