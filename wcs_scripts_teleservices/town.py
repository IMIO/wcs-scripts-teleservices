# -*- coding: utf-8 -*-
import ast
import datetime
import operator
import re
from datetime import date, datetime, timedelta
from decimal import Decimal
import json

binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
}


def find_week(params):
    week = params.get("week")
    lst = params.get("lst")
    ### lst sample : ['S27_01/07/2020', 'S27_02/07/2020', 'S27_03/07/2020']
    return [day for day in lst if week in day]


class Town(object):
    def __init__(self, variables):
        self.variables = variables
        self.class_name = "Town"
        self.form_name = variables.get("form_name")
        self.user_zipcode = variables.get("session_user_var_zipcode")
        self.user_birthplace = variables.get("session_user_var_birthplace")
        self.user_wedding_cities = (
            variables.get("session_user_var_wedding_cities") or ""
        )
        self.user_title = variables.get("session_user_var_title")
        self.strong_authentication = (
            variables.get("session_user_var_verified_fields") or None
        )
        self.strong_authenticated_fields = [] if variables.get('session_user') is None else getattr(variables.get('session_user'),"verified_fields",[])
        self.form_objects = variables.get("form_objects")
        try:
            self.form_slug = variables.get("form_slug")
        except NameError:
            self.form_slug = None

    def get_form_slug(self):
        return self.form_slug

    def get_form_name(self):
        return self.form_name

    def dt_to_date(self, dt, format_date="%Y-%m-%d", format_time="%H:%M:%S"):
        return datetime.strptime(dt, "{0} {1}".format(format_date, format_time)).date()

    def is_strong_authentication(self, *args):
        if "_niss" in self.strong_authenticated_fields:
            return "True"
        else:
            return "False"

    # Méthode qui sert à retourner un texte accompaggé d'un résultat.
    # valeur : Un nombre
    # texte : un article (par exemple)
    # coeff : un coéfficient multiplicateur
    # unit : unité de mesure
    # return sample = "[2] [certficats de domicile] = [10 (valeur*coeff)] [€]"
    def txt_ifn_zero(self, valeur, texte, coeff=1, unit=""):
        if str(valeur) == "0":
            return ""
        else:
            return (
                str(valeur)
                + " "
                + texte
                + " = "
                + str(int(valeur) * coeff)
                + " "
                + unit
            )

    def criteria_filtered_list(
        self,
        choices,
        value_to_test,
        criteria_to_test,
        choices_if_true,
        choices_if_false,
    ):
        if value_to_test == criteria_to_test:
            return [x for i, x in enumerate(choices) if i in choices_if_true]
        else:
            return [x for i, x in enumerate(choices) if i in choices_if_false]

    # Return number of days between two date
    # date1 : oldest date '%d/%m/%Y' format
    # date2 : newest date '%d/%m/%Y' format
    # if date1 older than date2, you get a postivie number of days.
    # return = Number of day between date2 and date1
    def diff_dates(self, date1, date2):
        try:
            try:
                d1 = datetime.strptime(date1, "%d/%m/%Y")
            except:
                d1 = datetime.combine(date1, datetime.min.time())
            d2 = datetime.strptime(date2, "%d/%m/%Y")
            diff = abs((d1 - d2).days)
            return str(diff)
        except:
            return "diff_dates_error"

    # Try to sum each row from a given column in a table (each value from the given column must be integer)
    # table_var : this is the variable name of the table in forms.
    # id_colonne : the id of the column in the table!
    # price : default value = 1.
    # return =  [sum of all row in given column] * price.
    def compute_dynamic_tab(self, table_var, id_colonne, price=1):
        result = 0
        if table_var is None:
            return str(result)
        else:
            try:
                id_col = int(id_colonne)
                for item in table_var:
                    value = item[id_col]
                    if value is None or value == "":
                        value = "0"
                    result = result + int(value)
                result = int(result) * int(price)
                return str(result)
            except Exception:
                return "compute_dynamic_tab : error" + str(table_var)

    # Imaginons un tableau. Chaque ligne est un motif et, dans la cellule de chaque motif, on peut y mettre un nombre d'exemplaires.
    # Il nous est impossible avec une telle représentation dans l'outil TS2 de faire un calcul directement sur le nombre d'exemplaire * 1 prix. (sauf si on affiche le prix en 2e colonne)
    # et de retourner un total complet.
    # Cette méthode apporte une solution à ce prolbème.
    # tab_var : Nom de la variable du tableau dans le formulaire
    # num_col : Numéro de colonne qui participe au calcul du résultat
    # memory_tab : Une liste avec la représentation en mémoire du tableau du formulaire [['id1','libelle1','price1'], ['id2','libelle2','price2'],..]
    def compute_tab_col(self, tab_var, num_col, memory_tab):
        error1 = "Erreur compute_tab_col : tableau en mem. different que tableau du formulaire."
        result = 0
        if len(tab_var) != len(memory_tab):
            result = error1
        else:
            cpt = 0
            for item in tab_var:
                try:
                    if item[int(num_col)] is None:
                        item = "0"
                    result = result + (
                        int(item[int(num_col)]) * int(memory_tab[cpt][2])
                    )
                    cpt = cpt + 1
                except Exception:
                    result = "Erreur compute_tab_col"
        return str(result)

    def validate_dynamic_tab_cells(
        self, table_var, id_colonne, regex_pattern, id_row="-1"
    ):
        retour = False
        id_col = int(id_colonne)
        is_date = False
        value = None
        if regex_pattern == "is_date":
            is_date = True
            regex_pattern = "(0?[1-9]|[12][0-9]|3[01])[-./](0?[1-9]|1[012])[-./]((1[1-9]|2[0-9])\\d\\d)"
        try:
            if id_row == "-1":
                for item in table_var:
                    value = item[id_col]
                    if item[0] == "":
                        pass
                    else:
                        if value == "" or value is None:
                            value = "NONE"
                        if re.match(regex_pattern, value):
                            retour = True
            else:
                id_r = int(id_row)
                value = table_var[id_r][id_col]
                if re.match(regex_pattern, value):
                    retour = True
            if retour is True and is_date is True:
                try:
                    separators = re.sub("[0-9]*", "", value)
                    annee = value.split(separators[0])[2]
                    mois = value.split(separators[0])[1]
                    jour = value.split(separators[0])[0]
                    newDate = datetime(int(annee), int(mois), int(jour))
                    retour = True
                except ValueError:
                    retour = False
            return retour
        except Exception:
            return False

    def compute_standard_motivations_table(
        self, motif_tab_var, lst_motifs_disponibles_var
    ):
        # In the stdrd motivation table, column0 is motivations' title and column1 is number of copies.
        col_title = 0
        col_nb_copies = 1
        total_price = Decimal("0")
        lst_selected_motifs = [
            x for x in motif_tab_var if x[0] != "" and x[0] is not None
        ]
        for selected_motif in lst_selected_motifs:
            for motif in lst_motifs_disponibles_var:
                if selected_motif[col_title] == motif["text"]:
                    nb_copies = (
                        selected_motif[col_nb_copies]
                        if selected_motif[col_nb_copies] != ""
                        else "1"
                    )
                    total_price += int(selected_motif[col_nb_copies]) * Decimal(
                        motif["price"]
                    )
        return str(total_price)

    def is_valid_belgian_nn(self, nn, can_be_none="False"):
        return self.is_valid_belgian_nrn(nn, can_be_none)

    def is_valid_belgian_nrn(self, nrn, can_be_none="False"):
        # nn => toujours 11 char meme apres 2000.
        if can_be_none == "True" and str(nrn) == "None":
            return True
        else:
            try:
                if nrn is None or nrn == "None":
                    nrn = "0"
                nrn = re.sub("[.-]", "", nrn)
                return (97 - int(nrn[:9]) % 97 == int(nrn[-2:])) or (
                    97 - int("2" + nrn[:9]) % 97 == int(nrn[-2:])
                )
            except ValueError:
                return False

    def is_valid_tva_number(self, tva_number):
        if not tva_number[:2].upper() == "BE":
            return False
        if not len(tva_number) == 12:
            if len(tva_number) == 11:
                tva_number = tva_number[:2] + "0" + tva_number[2:]
            else:
                return False
        if re.match("^[0-9]{10}$", tva_number[2:]):
            int_value = int(tva_number[2:10])
            check_digit = int(int_value / 97) * 97
            if (97 - (int_value - check_digit)) == int(tva_number[10:12]):
                return True
            else:
                return False

    def check_duplicate_field(self, varname):
        field_id = [
            x for x in self.form_objects.formdef.fields if x.varname == varname
        ][0].id
        result = bool(
            len(
                [
                    x
                    for x in self.form_objects.formdef.data_class().select()
                    if x.data.get(field_id) == globals().get("form_var_%s" % (varname))
                    and not x.is_draft()
                ]
            )
            == 0
        )

    # Birthdate like 07/01/1979
    # Birthdate unknow but good year=> nn like 40 00 00 955-23 (third, fourth, fifth and sixth params are 0 and 2 firsts is year of birthday.
    # Birthdate unknow => 00 00 01 003-85 (5 firsts number are 0 and sixth is 1
    # nn like 79010705741
    def check_birthday_in_nn(self, birthday, nn):
        if isinstance(birthday, datetime):
            birthday = datetime.strftime(birthday, "%d/%m/%Y")
        result = False
        try:
            # date unknow
            if birthday is None or birthday == "":
                result = "000001" == nn[:6]
            # year is knowing
            if nn.startswith(birthday[-2:] + "0000") or nn.startswith(
                "2" + birthday[-2:] + "000"
            ):
                result = birthday[-2:] in nn[0:3]
            # standart behaviour
            else:
                reversed_birthday_short_year = "".join(
                    [elt for elt in birthday.split("/")[::-1]]
                )[2:]
                result = nn[:6] == reversed_birthday_short_year
        except Exception:
            result = False
        return str(result)

    def authentication_delivrance_items_visibility(self, datasource, auth=None):
        if len(auth) > 0:
            for elm in datasource:
                if "commune" not in elm["id"]:
                    elm["disabled"] = False
            return datasource
        return datasource

    def eid_conditional_datasource(self, ds_if_true, ds_if_false):
        return self.conditional_datasource(
            str(self.strong_authentication), "True", "=", ds_if_true, ds_if_false
        )

    def conditional_datasource(
        self, variable, value_to_test, operator, ds_if_true, ds_if_false
    ):
        if operator == "in":
            if value_to_test in variable:
                return ds_if_true
            else:
                return ds_if_false
        if operator == "=":
            if value_to_test == variable:
                return ds_if_true
            else:
                return ds_if_false

    def is_valid_iban(self, iban):
        ibanValidationModulo = 97
        iban = iban.upper()
        iban = iban.replace(" ", "")
        if len(iban) < 5:
            return False
        modifiedIban = iban[4: len(iban)] + iban[0:4]
        numericIbanString = ""
        for c in modifiedIban:
            currentCharCode = ord(c)
            # Integer
            if (currentCharCode > 47) and (currentCharCode < 58):
                numericIbanString = numericIbanString + c
            # Char
            elif (currentCharCode > 64) and (currentCharCode < 91):
                value = currentCharCode - 65 + 10
                numericIbanString = numericIbanString + str(value)
            else:
                return False
        previousModulo = 0
        for i in range(0, len(numericIbanString), 5):
            subpart = str(previousModulo) + "" + numericIbanString[i: i + 5]
            previousModulo = int(subpart) % ibanValidationModulo
        return previousModulo == 1

    def is_agent(self):
        return (
            globals().get("session_user")
            and globals().get("session_user").can_go_in_backoffice()
        )

    # In comment field, we can do thing like that : [script.commune "somme" form_var_value1 form_var_value2 form_var_value3]
    def somme(self, *args):
        result = Decimal("0")
        for item in args:
            try:
                result = result + Decimal(item)
            except Exception:
                pass
        return str(result)

    def test_globals(self, *args):
        return self.variables.get("form_var_prenom") or " "

    def ifelse(self, *args):
        return args[0] or args[1]

    # Decimal usage? :https://stackoverflow.com/questions/35406257/convert-ast-num-to-decimal-decimal-for-precision-in-python
    def arithmeticEval(self, s):
        special_chars_to_remove = "()/+-*"
        string_without_special = s
        for c in special_chars_to_remove:
            string_without_special = string_without_special.replace(c, " ")
        lst_elem = string_without_special.split(" ")
        lst_vars = [
            elem
            for elem in lst_elem
            if elem.startswith("form_var_") or elem.startswith("form_option_")
        ]
        for elem in lst_vars:
            s = s.replace(elem, str(self.variables.get(elem) or 0))
        s = s.strip()
        node = ast.parse(s, mode="eval")

        def _eval(node):
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            elif isinstance(node, ast.Str):
                return node.s
            elif isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.BinOp):
                try:
                    return binOps[type(node.op)](_eval(node.left), _eval(node.right))
                except Exception:
                    return "-1"
            else:
                raise Exception("Unsupported type {}".format(node))

        return _eval(node.body)

    def safe_total(self, formula):
        return str(self.arithmeticEval(formula))

    def total(self, formula=None):
        if formula is not None:
            retour = self.safe_total(formula)
        else:
            retour = (
                Decimal(globals().get("form_option_cost"))
                + Decimal(globals().get("form_var_motifs_price"))
            ) * int(globals().get("form_var_nb_exemplaire"))
        return str(retour)

    def towntime_add_type_rdv_dic_key(self, lst_type_rdv):
        numeric_id = 1
        new_lst = []
        for item in lst_type_rdv:
            item["numericid"] = str(numeric_id)
            numeric_id = numeric_id + 1
            new_lst.append(item)
        return new_lst

    def towntime_are_nn_all_differents(self, lst_nn):
        lst_without_none = [nn for nn in lst_nn if nn is not None]
        return len(lst_without_none) == len(set(lst_without_none))

    # exemple dt_format : %Y-%m-%d ou %d/%m/%Y ,...
    def struct_time_to_str(self, struct_time, dt_format):
        str = datetime(*struct_time[:3]).strftime(dt_format)
        return str

    # deprecated
    # def get_dates_of_week_number(self, numweek, lst_days):
    #     days = list(filter(find_week, {"week":numweek, "lst":lst_days}))
    #     firstday = datetime.strptime(days[0].split("_")[1], "%d/%m/%Y")
    #     lastday = datetime.strptime(days[-1:].split("_")[1], "%d/%m/%Y")
    #     str_firstday = firstday.strftime("%A %d/%m/%Y")
    #     str_lastday = lastday.strftime("%A %d/%m/%Y")
    #     return [str_firstday, str_lastday]

    def get_dates_of_week_number(self, numweek, year):
        if numweek.upper().startswith("S"):
            d = "W{}/{}".format(numweek[1:], year)
        else:
            d = "W{}/{}".format(numweek, year)
        monday = datetime.strptime("1/" + d, "%w/W%W/%Y")
        delta = timedelta(days=5)
        friday = monday + delta
        return [monday.strftime("%d/%m/%Y"), friday.strftime("%d/%m/%Y")]

