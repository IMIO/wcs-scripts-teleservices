# -*- coding: utf-8 -*-
from decimal import Decimal
import sys
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')
import re

if 'town' in sys.modules:
    del sys.modules['town']

import town


class Waterloo(town.Town):

    def __init__(self, variables={}):
        globals().update(variables)
        self.centre_recreatif_supplement_piscine = 0
        self.description = ''
        self.cr_lst_week_choices = [globals().get('form_var_semaineE1_raw'),
                           globals().get('form_var_semaineE2_raw'),
                           globals().get('form_var_semaineE3_raw'),
                           globals().get('form_var_semaineE4_raw'),
                           globals().get('form_var_semaineE5_raw'),
                           globals().get('form_var_semaineE6_raw')
                        ]
        self.cr_lst_activites_choices = [globals().get('form_var_activite_comp_E1_raw'),
                                globals().get('form_var_activite_comp_E2_raw'),
                                globals().get('form_var_activite_comp_E3_raw'),
                                globals().get('form_var_activite_comp_E4_raw'),
                                globals().get('form_var_activite_comp_E5_raw'),
                                globals().get('form_var_activite_comp_E6_raw')
                             ]
        self.cr_lst_birthday_children = [globals().get('form_var_birthdayE1'),
                                globals().get('form_var_birthdayE2'),
                                globals().get('form_var_birthdayE3'),
                                globals().get('form_var_birthdayE4'),
                                globals().get('form_var_birthdayE5'),
                                globals().get('form_var_birthdayE6')
                            ]
        self.cr_nb_enfants = globals().get('form_var_NB_Enfants') or '0'
        self.cr_promotion = globals().get('form_var_promotion') or 'Non'
        super(Waterloo, self).__init__(variables=globals())

    def centre_recreatif_compute_desc(self, *args):
        return self.centre_recreatif_compute(self.cr_nb_enfants, 
                                             self.cr_lst_week_choices, self.cr_promotion)

    def total_desc(self, *args):
        total_semaine_hors_activite = self.centre_recreatif_compute(self.cr_nb_enfants, 
                                            self.cr_lst_week_choices, self.cr_promotion)
        total_activites = self.centre_recreatif_activites_compute(self.cr_nb_enfants,
                                            self.cr_lst_activites_choices)
        supp_piscine = self.centre_recreatif_supp_piscine_5_ans(self.cr_lst_birthday_children,
                                            self.cr_lst_week_choices)
        exceptions_piscine = self.centre_recreatif_piscine_exceptions(self.cr_lst_birthday_children,
                                            self.cr_lst_week_choices)
        return str(round(Decimal(total_semaine_hors_activite) + 
                         Decimal(total_activites) + 
                         Decimal(supp_piscine) - 
                         Decimal(exceptions_piscine),2))


    def centre_recreatif_compute_v2(self, nb_enfants, lst_week_choices, promotion='Non'):    
        import collections
        total = Decimal('0')
        tarif_appliquer = None
        details = ''
        liste_stages = filter(None, lst_week_choices)
        all_stages_id_for_all_children = [item for liste_stages in liste_stages for item in liste_stages if item is not None]
        dic_prices = {
                'S1_2018':[40,75,90],
                'S2_2018':[40,75,90],
                'S3_2018':[40,75,90],
                'S4_2018':[40,75,90], 
                'S5_2018':[40,75,90], 
                'S6_2018':[40,75,90], 
                'S7_2018':[32,60,72], 
                'S8_2018':[40,75,90]
        }
        participations = collections.Counter(all_stages_id_for_all_children)
        for p in participations:
            semaine = p
            print(semaine,participations[p])
            if participations[p] >= 3:
                total = total + dic_prices.get(semaine)[2]
            else:
                total = total + dic_prices.get(semaine)[participations[p] -1]
        return total

    def centre_recreatif_compute(self, nb_enfants, lst_week_choices, promotion='Non'):
        total = self.centre_recreatif_compute_v2(nb_enfants, lst_week_choices, promotion='Non')
        # total = Decimal('0')
        tarif_appliquer = None
        details = ''
        # format du prix d'un centre recreatif pour un enfant
        # form_var_semaineE1_0_prix1
        liste_stages = filter(None, lst_week_choices)
        all_stages_id_for_all_children = [item for liste_stages in liste_stages for item in liste_stages if item is not None]
        for enfant in range(1,int(nb_enfants) + 1):
            if lst_week_choices[enfant - 1] is not None:
                lst_id_stages_enfant = lst_week_choices[enfant - 1]
                nb_stages = len(lst_id_stages_enfant)
                details += 'Enfant {0}<ul>'.format(enfant)
                for stage in range(0, nb_stages):
                    id_stage = lst_id_stages_enfant[stage]
                    cpt_children_for_this_stage = all_stages_id_for_all_children.count(id_stage)
                    if int(cpt_children_for_this_stage) == 1:
                        tarif_appliquer = 'prix1'
                    if int(cpt_children_for_this_stage) == 2:
                        tarif_appliquer = 'prix2'
                    if int(cpt_children_for_this_stage) >= 3:
                        tarif_appliquer = 'prix3'
                    semaine = globals().get('form_var_semaineE{0}'.format(enfant)).split(',')[stage]
                    price_varname = 'form_var_semaineE{0}_{1}_{2}'.format(enfant, stage, tarif_appliquer)
                    price_for_current_stage_and_child = globals().get(price_varname)
                    if price_for_current_stage_and_child is not None:
                        details += '<li>{0} - {1} Eur</li>'.format(semaine, price_for_current_stage_and_child)                        
                        # total = total + Decimal(price_for_current_stage_and_child)
                    else:
                        total = 'error : Stage : child {0}, var {1}, value = {2}'.format(enfant, price_varname, price_for_current_stage_and_child)
                        break
                details += '</ul>'
            else:
                total = 'error : Stage : child {0}'.format(enfant)
                break
        txt_promo = ''
        if promotion == 'Oui' and globals().get('form_var_lst_promo_raw') == '0':
            txt_promo = 'Promotion : 50% sur le total des semaines. (hors activités complémentaires)'
        if promotion == 'Oui' and globals().get('form_var_lst_promo_raw') == '1':
            txt_promo = 'Promotion : Inscription gratuite pour les semaines. (hors activités complémentaires)'
        self.description += '<p>-------------</p><p><b>Semaines de plaine :</b></p>{0}<p>{1}</p>'.format(details, txt_promo)
        return str(total) if promotion == 'Non' else '0.00' if globals().get('form_var_lst_promo_raw') == '1' else str(total / 2)

    def centre_recreatif_activites_compute(self, nb_enfants, lst_activites_choices):
        total = Decimal('0')
        # format du prix d'une activite par enfant
        # form_var_activite_comp_E1_0_prix
        details = ''
        has_activite = False
        for enfant in range(1,int(nb_enfants) + 1):
            if lst_activites_choices[enfant - 1]:
                details += 'Enfant {0}<ul>'.format(enfant)
                nb_activites = len(lst_activites_choices[enfant - 1])
                for activite in range(0, nb_activites):
                    activite_text = globals().get('form_var_activite_comp_E{0}'.format(enfant)).split(',')[activite]
                    price_varname = 'form_var_activite_comp_E{0}_{1}_prix'.format(enfant, activite)
                    price_for_current_activite_and_child = globals().get(price_varname)
                    if price_for_current_activite_and_child is not None:
                        has_activite = True
                        details += '<li>{0} - {1} Eur</li>'.format(activite_text, price_for_current_activite_and_child)
                        total = total + Decimal(price_for_current_activite_and_child)
                    else:
                        total = 'error1 : Activite : child {0}, var {1}, value = {2}'.format(enfant, price_varname, price_for_current_activite_and_child)
                        break
                details = '{0}{1}'.format(details,'</ul>')
        if has_activite is True:
            self.description += '<p>-------------</p><p><b>Activites complementaires :</b></p>{0}'.format(details)

        return str(total)

    def centre_recreatif_supp_piscine_5_ans(self, lst_birthday_children,lst_week_choices=[],supplement=2.3):
        self.centre_recreatif_supplement_piscine = supplement
        total_supp_piscine = 0
        from datetime import datetime
        from dateutil import relativedelta
        num_enfant = 1
        has_swimming_pool = False
        details = ''
        for birthday in lst_birthday_children:
            if birthday is not None and len(birthday) > 0:
                dt_birthday = datetime.strptime(birthday, '%d/%m/%Y')
                #dt_2013 = datetime.strptime('01/01/2013', '%d/%m/%Y')
                today = datetime.today()
                difference = relativedelta.relativedelta(today, dt_birthday)
                if difference.years >= 5:
                    has_swimming_pool = True
                    nb_semaines_par_enfant = len(lst_week_choices[num_enfant -1])
                    details += '<ul><li>Enfant {0}  : {1} Eur</li></ul>'.format(num_enfant, (supplement * nb_semaines_par_enfant))
                    total_supp_piscine = total_supp_piscine + (supplement * nb_semaines_par_enfant)
            num_enfant = num_enfant + 1
        if has_swimming_pool is True:
            self.description += '<p>-------------</p><p><b>Frais de piscine :</b></p>{0}'.format(details)
        return total_supp_piscine

    def centre_recreatif_piscine_exceptions(self, lst_birthday_children,lst_week_choices=[]):
        from datetime import datetime
        from dateutil import relativedelta
        num_enfant = 1
        has_swimming_pool_exceptions = False
        details = ''
        total_remise = 0
        for birthday in lst_birthday_children:
            if birthday is not None and len(birthday) > 0:
                dt_birthday = datetime.strptime(birthday, '%d/%m/%Y')
                today = datetime.today()
                difference = relativedelta.relativedelta(today, dt_birthday)
                if difference.years == 6 or difference.years == 7:
                    semaines_enfant = lst_week_choices[num_enfant - 1]
                    # 19/07 et du 16/08
                    if 'S3_2018' in semaines_enfant or 'S7_2018' in semaines_enfant:
                        has_swimming_pool_exceptions = True
                        total_remise = total_remise + self.centre_recreatif_supplement_piscine 
            num_enfant = num_enfant + 1
        details += '<ul><li>Montant à soustraire  : -{0} Eur</li></ul>'.format(total_remise)
        if has_swimming_pool_exceptions is True:
            self.description += '<p>-------------</p><p><b>Annulation des frais de piscine pour les enfant de 6 et 7 ans :</b></p>{0}'.format(details)
        return str(total_remise)


    def get_centre_recreatif_activites(self, lst_week_choices, datasource):
        new_datasource = []
        if datasource is not None:
            if type(datasource) is not list:
                if datasource.get('data') is not None:
                    datasource = datasource.get('data')
            if lst_week_choices is not None:
                for item in datasource:
                    for semaine in lst_week_choices:
                        if semaine in item.get('id'):
                            new_datasource.append(item)
        return new_datasource

    def generate_structured_communication(self, transaction_id):
        split = transaction_id.split('-')
        transaction_id = split[0] + split[1] + str(sum([ int(c) for c in split[0] ]))
        count = 10 - len(str(transaction_id))
        for i in range(0,count):
            transaction_id = "{}{}".format('0',transaction_id)
        control = int(transaction_id) % 97
        str_control = str(control)
        if control < 10:
            str_control = "{}{}".format("0",str_control)
        com = "{}{}".format(transaction_id, str_control)
        # if int(com[:9]) % 97 == int(com[-2:]:
        # test if valid structured comm.
        return "{}/{}/{}".format(com[0:3], com[3:7], com[7:12])

    def is_at_least_one_activity_by_week(self, enfant, ds=None):
        lst_week_choices = globals().get('form_var_semaine{0}_raw'.format(enfant))
        list_activites_affichees = self.get_centre_recreatif_activites(lst_week_choices, ds)
        selected_weeks = globals().get('form_var_semaine{0}_raw'.format(enfant))    
        selected_activities = globals().get('form_var_activite_comp_{0}_raw'.format(enfant))
        set_weeks = set(selected_weeks)
        sel_activities = [x[:-2] for x in selected_activities]
        set_activities = set()
        for item in sel_activities:
            if item not in set_activities:
                set_activities.add(item)
            else:
                return False
        if list_activites_affichees is not None:
            if len(set_activities) != len(set([dic.get('id')[:-2] for dic in list_activites_affichees])):
                return False
            else:
                return True
        else:
            return True
        # set_activities = set([x[:-2] for x in selected_activities])
        # nb_diff = len(set_activities.difference(set_weeks))
        # if nb_diff == 0:
        #    return True
        #else:
        #    return False



if globals().get('args') is None:
    test = True
else:
    if args[0] == 'get_payement_details':
        nb_children = globals().get('form_var_NB_Enfants') or 0
        lst_week_choices = [globals().get('form_var_semaineE1_raw'), globals().get('form_var_semaineE2_raw'), globals().get('form_var_semaineE3_raw'), globals().get('form_var_semaineE4_raw'), globals().get('form_var_semaineE5_raw'), globals().get('form_var_semaineE6_raw')] or []
        lst_activites_choices = [globals().get('form_var_activite_comp_E1_raw'), globals().get('form_var_activite_comp_E2_raw'), globals().get('form_var_activite_comp_E3_raw'), globals().get('form_var_activite_comp_E4_raw'), globals().get('form_var_activite_comp_E5_raw'), globals().get('form_var_activite_comp_E6_raw')] or []
        lst_birthday_children = [globals().get('form_var_birthdayE1'),  globals().get('form_var_birthdayE2'), globals().get('form_var_birthdayE3'), globals().get('form_var_birthdayE4'), globals().get('form_var_birthdayE5'), globals().get('form_var_birthdayE6')] or []
        w = Waterloo()
        w.centre_recreatif_compute(nb_children, lst_week_choices, globals().get('form_var_promotion'))
        w.centre_recreatif_activites_compute(nb_children, lst_activites_choices)
        w.centre_recreatif_supp_piscine_5_ans([globals().get('form_var_birthdayE1'),globals().get('form_var_birthdayE2'),globals().get('form_var_birthdayE3'),globals().get('form_var_birthdayE4'),globals().get('form_var_birthdayE5'),globals().get('form_var_birthdayE6')], lst_week_choices)
        w.centre_recreatif_piscine_exceptions([globals().get('form_var_birthdayE1'),globals().get('form_var_birthdayE2'),globals().get('form_var_birthdayE3'),globals().get('form_var_birthdayE4'),globals().get('form_var_birthdayE5'),globals().get('form_var_birthdayE6')], lst_week_choices)
        result = '<p>{0}</p>'.format(w.description)
    else:
        current_commune = Waterloo()
        function = args[0]
        functionList = {function: getattr(current_commune,function)}
        if len(args) > 1:
            parameters = args[1]
            if isinstance(parameters, dict):
                result = functionList[function](**parameters)
            else:
                params = args[1:]
                result = functionList[function](*params)
        else:
            result = functionList[function]()

