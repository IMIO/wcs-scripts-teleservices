# -*- coding: utf-8 -*-
from decimal import Decimal
import os
import sys


if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))


def cout_accueil(data):
    try:
        return Decimal(data.get("form_option_cout_garderie")) * len(
            (
                data.get("form_var_garderie_s1_raw") or []
            )
            + (
                data.get("form_var_garderie_s2_raw") or []
            )
            + (
                data.get("form_var_garderie_s3_raw") or []
            )
            + (
                data.get("form_var_garderie_s4_raw") or []
            )
            + (
                data.get("form_var_garderie_s5_raw") or []
            )
            + (
                data.get("form_var_garderie_s6_raw") or []
            )
        )
    except:
        return "-1"


def cout_reservation(data):
    try:
        return Decimal(
            data.get("form_option_cout_resident")
            if data.get("form_var_code_postal") == commune_cp
            else data.get("form_option_cout_non_resident")
        ) * len(data.get("form_var_semainestage_raw") or "1")
    except:
        return "-1"


if args[0] == "couttotal":
    result = str(Decimal(cout_accueil(vars())) + Decimal(cout_reservation(vars())))

if args[0] == "coutaccueil":
    result = str(cout_accueil(vars()))

if args[0] == "coutreservation":
    result = str(cout_reservation(vars()))
