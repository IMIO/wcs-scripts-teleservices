# Scripts for map statement management:
# close_demands.py
# has_close_demands.py
# similar_list.py
# similar_map.py
# usage on a form  : str(int(script.get_similars_observations('count')) + 1)


import os
import sys

import close_demands

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))


result = ""
list_sous_domaines = [
    "var_sous_domaine_proprete",
    "var_sous_domaine_avaloir",
    "var_sous_domaine_voirie",
    "var_sous_domaine_graffiti",
    "var_sous_domaine_espace_vert",
    "var_sous_domaine_signalisation",
    "var_sous_domaine_mobilier_urbain",
    "var_sous_domaine_voirie",
]


def get_similars_observations_count(data):
    coords = close_demands.get_coords(data)
    result = 0
    if coords:
        for item in close_demands.get_close_demands(form_objects.formdef, coords, data):
            structured_item = item.get_as_dict()
            if structured_item["var_incident"] == form_var_incident:
                for sous_domaine in list_sous_domaines:
                    if "sous_domaine" in structured_item:
                        if structured_item[
                            sous_domaine
                        ] is not None and structured_item[sous_domaine] == data.get(
                            "form_{}".format(sous_domaine)
                        ):
                            result = result + 1
    return str(result)


# form_status : contient le status courant de la demande.
def get_similars_observations_mails(data):
    coords = close_demands.get_coords(data)
    lst_mails = []
    result = ""
    if coords:
        for item in close_demands.get_close_demands(form_objects.formdef, coords, data):
            structured_item = item.get_as_dict()
            if structured_item["var_incident"] == form_var_incident:
                for sous_domaine in list_sous_domaines:
                    if "sous_domaine" in structured_item:
                        if structured_item[
                            sous_domaine
                        ] is not None and structured_item[sous_domaine] == data.get(
                            "form_{}".format(sous_domaine)
                        ):
                            if (
                                "var_mail_for_similar_observation" in structured_item
                                and structured_item["var_mail_for_similar_observation"]
                                is not None
                            ):
                                lst_mails.append(formdata.get_field_view_value(field))
        result = ",".join(lst_mails)
    return result


def set_data_on_first_observation(data, signalement_similaire):
    # Set first observation on current demand.
    # form_var_first_observation = signalement_similaire
    # structured_item =  formdata.get_as_dict()
    formdef = form_objects.formdef
    cpt_signalements = 0
    for formdata in formdef.data_class().select():
        guess_form_number = globals().get(
            "form_number_raw", max([int(i) for i in formdata.keys()])
        )
        if str(formdata.id) == str(signalement_similaire):
            for field in formdef.get_all_fields():
                if field.varname is not None:
                    if (
                        "str_all_mails" == field.varname
                        and data.get("form_var_mail_for_similar_observation")
                        is not None
                    ):
                        if (
                            field.id not in formdata.data.keys()
                            or formdata.data[field.id] is None
                        ):
                            formdata.data[
                                field.id
                            ] = form_var_mail_for_similar_observation
                        else:
                            lst_mails = set(
                                "{},{}".format(
                                    formdata.data[field.id] or "",
                                    form_var_mail_for_similar_observation,
                                ).split(",")
                            )
                            formdata.data[field.id] = ",".join(lst_mails)
                    if "signalements" == field.varname:
                        if (
                            field.id not in formdata.data.keys()
                            or formdata.data[field.id] is None
                        ):
                            formdata.data[field.id] = str(guess_form_number)
                            cpt_signalements = 1
                        else:
                            lst_signalements = str(formdata.data[field.id] or "").split(
                                ","
                            )
                            if str(guess_form_number) not in lst_signalements:
                                formdata.data[field.id] = "{},{}".format(
                                    formdata.data[field.id] or "", guess_form_number
                                )
                            cpt_signalements = len(lst_signalements) + 1
                    if "cpt_signalements" == field.varname:
                        formdata.data[field.id] = str(cpt_signalements)
                formdata.store()
    return str(signalement_similaire)


if args[0] == "mail":
    result = get_similars_observations_mails(vars())
if args[0] == "count":
    result = get_similars_observations_count(vars())
if args[0] == "set_on_first_observation":
    result = set_data_on_first_observation(vars(), args[1])
