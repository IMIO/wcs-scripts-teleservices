# -*- coding: utf-8 -*-
import operator
import re
import sys
from decimal import Decimal


sys.path.insert(0, "/var/lib/wcs/scripts")
sys.path.insert(0, "/var/lib/wcs-au-quotidien/scripts")
if "town" in sys.modules:
    del sys.modules["town"]
import town


class Namur(town.Town):
    def __init__(self):
        # Le cout des demarches de pop/ec s'effectue comme suit : 
        # Si commande pour sois-même : Si on habite dans VALID_CP alors gratos sinon payant.
        # Si commande pour un tiers : 
        #                           - Si on est un "privé" alors, gratos si on est dans VALID_CP
        #                           - Si on est un "professionnel" alors, gratos uniquement pour les tiers dans VALID_CP sinon payant.
        self.VALID_CP = ["5000", "5001", "5002", "5003", "5004", "5020", "5021", "5022", "5024", "5100", "5101"]
        super(Namur, self).__init__(variables=globals())

    # Get a readable list formated like : [('id1','libelle1','price1'),('id2','libelle2','price2')]
    # return a less readable but more functionnal list like :  [('id1_price1','libelle1'),('id2_price2','libelle2')] to populate multiselectlist or multicheckboxlist.
    def get_list_with_formated_id_price(self, choices):
        try:
            new_list = [(elem[0] + "_" + elem[2], elem[1]) for elem in choices]
            return new_list
        except Exception:
            return "Invalid parameters. Please, verify your list of choices {'choices':[('ID1','TITLE1','PRICE1'), ('ID2','TITLE2','PRICE2'),...]}"

    # Compute price tanks to id_price
    # select must be the less readable list : (id1_price1, id2_price2, id3_price3)
    def compute_prices_list(self, select):
        try:
            return sum([int((elem.split("_"))[1]) for elem in select])
        except Exception:
            return "Invalid result"

    # Permet de transformer une datasrc imagin�e comme ceci : [[id1,title1,prix1], [id2,title2, prix2]]
    # vers une liste comme celle-ci : [[id1_prix1, title1], [id2_prix2, title2]]
    def datasource_with_price_and_id(self, datasrc):
        nouvelle_liste = []
        for item in datasrc:
            new_item = [item[0] + "_" + str(item[2]), item[1]]
            nouvelle_liste.append(new_item)
        return nouvelle_liste

    # Permet, à partir d'une liste alimentée par un dictionnaire avec, par exemple, un id, un text et un prix
    # et à partir d'un tableau qui reprend certains intitulés de la liste et qui demande, par exemple un nombre d'exemplaire pour les items de la liste
    # de renvoyer le total
    # table_var : La variable du tableau qui contient le nb d'exemplaires pour les articles de la liste à choix multiple préalablement sélectionnés.
    # list_var_raw : La variable "raw" de la liste d'item
    # list_name : str qui contient le nom de la variable de la liste d'item
    # rich_list_properties_name : Notre liste, alimentée par un dictionnaire est enrichie par une propriétés "price" ==> rich_liste_properties_name = "price"
    # table_col : Spécifie la colonne du tableau qui sera utilisée dans le calcul avec la propriété enrichie de la liste.
    def compute_price(
        self, table_var, list_var_raw, list_name, rich_list_properties_name, table_col=0
    ):
        filtered_table = []
        for elem in table_var:
            try:
                filtered_table.append(int(elem[table_col]))
            except:
                pass
        list_motifs = []
        i = 0
        while i < len(list_var_raw):
            list_motifs.append(
                int(
                    globals().get(
                        list_name + "_" + str(i) + "_" + rich_list_properties_name
                    )
                )
            )
            i = i + 1
        return str(sum(map(operator.mul, list_motifs, filtered_table)))

    def compute_standard_motivations_table_args(self, *args):
        values = args
        retour = ''
        if globals().get(values[0]) is not None and globals().get(values[1]) is not None:
            retour = str(self.compute_standard_motivations_table(globals().get(values[0]), globals().get(values[1]), globals().get("form_option_before2020")))
        return retour

    # before_2020 : Pour la gestion des actes avant 2020 ou apres 2020
    # integration des nouvelles reglementations de la BAEC.
    # result = un coût
    def compute_standard_motivations_table(self, motif_tab_var, lst_motifs_disponibles_var, before_2020="True"):
        cp_demandeur = (globals().get("form_var_cp_demandeur") or '').strip()
        if globals().get("form_var_nn_statut") == "Privé" and cp_demandeur in self.VALID_CP:
            result = Decimal("0.00")
        else:
            # Il n'y a pas de tableau de motif sur l'acte de reconnaissance d'enfant.
            if "acte-de-reconnaissance-d-enfant" in globals().get("form_slug"):
                result = self.total_with_tab_tiers("form_var_nb_exemplaire", "form_option_cost", "form_var_tableau_tiers")
            else:
                nb_tiers = len(globals().get('form_var_tableau_tiers')) if globals().get('form_var_tableau_tiers') is not None else 1
                result = Decimal("0")
                if str(before_2020) == "True" or before_2020 is None:
                    result = nb_tiers * Decimal(super(Namur, self).compute_standard_motivations_table(motif_tab_var, lst_motifs_disponibles_var))
                else:
                    nb_doc = 1 if motif_tab_var is None else sum([0 if e[1] is None or e[1] == "" else int(e[1]) for e in motif_tab_var])
                    if globals().get("form_var_tableau_tiers") is not None:
                        for tiers in globals().get("form_var_tableau_tiers"):
                            if "acte-de-divorce" in globals().get("form_slug"):
                                code_postal_tiers = tiers[7]
                            elif "acte-de-mariage" in globals().get("form_slug"):
                                code_postal_tiers = tiers[6]
                            else:
                                code_postal_tiers = tiers[4]
                            # En tant que demandeur privé n'habitant pas à Namur et commandant pour des pers tiers habitant à Namur ou non, les démarches seront payantes
                            if globals().get("form_var_nn_statut")=="Privé" or code_postal_tiers.strip() not in self.VALID_CP:
                                result = result + Decimal(globals().get("form_option_cost"))
                        result = nb_doc * result
                    else:
                        if cp_demandeur.strip() not in self.VALID_CP:
                            result = nb_doc * Decimal(globals().get("form_option_cost"))
        return result

    # global_cost != 0 seulement si on n'utilise pas les motifs (motif_tab_var is None and lst_motifs_disponibles_var is None)
    # global_nb_exemplaire != 0 seulement si on n'utilise pas les motifs (motif_tab_var is None and lst_motifs_disponibles_var is None)
    def compute_virement(
        self,
        motif_tab_var,
        lst_motifs_disponibles_var,
        postage_fees,
        global_cost="0",
        global_nb_exemplaire="0",
    ):
        nb_tiers = (
            len(globals().get("form_var_tableau_tiers"))
            if globals().get("form_var_tableau_tiers") is not None
            else 1
        )
        # Namur default value (each 5 doc in a letter, add new fees)
        max_doc_in_letter = 5
        if (
            motif_tab_var is None
            and lst_motifs_disponibles_var is None
            and global_cost != "0"
            and global_nb_exemplaire != "0"
        ):
            total_price = Decimal(global_cost) * int(global_nb_exemplaire) * nb_tiers
            # nb_documents to compute postage fee (*nb_tiers) to compute with number of people
            nb_documents = int(global_nb_exemplaire) * nb_tiers
        else:
            total_price = Decimal(
                self.compute_standard_motivations_table(
                    motif_tab_var, lst_motifs_disponibles_var
                )
            )
            nb_documents = int(self.compute_dynamic_tab(motif_tab_var, 1)) * nb_tiers
        nb_letter = int(nb_documents / max_doc_in_letter) + (
            ((nb_documents % max_doc_in_letter) > 0) and 1 or 0
        )
        # compute fees
        postage_fees = int(nb_letter) * Decimal(postage_fees)
        return str(total_price + postage_fees)

    def generate_structured_communication(transaction_id):
        split = transaction_id.split("-")
        transaction_id = split[0] + split[1] + str(sum([int(c) for c in split[0]]))
        count = 10 - len(str(transaction_id))
        for i in range(0, count):
            transaction_id = "{}{}".format("0", transaction_id)
        control = int(transaction_id) % 97
        str_control = str(control)
        if control < 10:
            str_control = "{}{}".format("0", str_control)
        com = "{}{}".format(transaction_id, str_control)
        # if int(com[:9]) % 97 == int(com[-2:]:
        # test if valid structured comm.
        return "{}/{}/{}".format(com[0:3], com[3:7], com[7:12])

    def html_table(self, table):
        str_table = "<table>"
        for item in table:
            str_table = "{}{}".format(str_table, "<tr>")
            str_table = "{}{}{}{}".format(str_table, "<td>", item[0], "</td>")
            str_table = "{}{}{}{}".format(str_table, "<td>", item[0], "</td>")
            str_table = "{}{}".format(str_table, "</tr>")
        str_table = "{}{}".format(str_table, "</table>")
        return str_table

    # args : form_var_nb_exemplaire, form_option_cost, form_var_tableau_tiers
    # form : acte reconnaissance enfant.
    def total_with_tab_tiers(self, *args):
        nb_tiers = 0
        result = ""
        # commande pour un tiers
        if globals().get(args[2]) is not None:
            for tiers in globals().get(args[2]):
                if tiers[4].strip() not in self.VALID_CP:
                    nb_tiers = nb_tiers + 1
            result = str(int(globals().get(args[0]) or '1') * Decimal(globals().get(args[1]) or '1')* nb_tiers)
        # commande pour sois-meme
        else:
            if (globals().get("form_var_cp_demandeur") or '').strip() not in self.VALID_CP:
                result = str(int(globals().get(args[0]) or '1') * Decimal(globals().get(args[1]) or '1'))
            else:
                result = '0.00'
        return result
        # return str(int(globals().get(args[0]) or '1') * Decimal(globals().get(args[1]) or '1')* (len(globals().get(args[2]) or '/')))


current_commune = Namur()
function = args[0]

functionList = {function: getattr(current_commune, function)}
if args[1] is not None:
    parameters = args[1]
    if isinstance(parameters, dict):
        result = functionList[function](**parameters)
    else:
        params = args[1:]
        result = functionList[function](*params)
else:
    result = functionList[function]()
