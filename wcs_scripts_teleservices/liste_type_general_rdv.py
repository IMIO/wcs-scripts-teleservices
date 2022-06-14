import requests
import json
import re


def tri_rendez_vous(liste):
    """
    :param liste: liste json des types de rendez-vous avec le nombre de personnes encodé de la façon' - 1 personne' + pluriel ou ' pour 1 personne' + pluriel
    :return: liste du type de rendez-vous sans le nombre de personnes
    """
    
    return list(set([re.sub(r" (pour|-) [0-9]+ personne(s)?$", "", x["text"]) for x in liste["data"]]))


try:
    headers = {'Accept': 'application/json'}

    # args[0] == l'url des types de rendez-vous
    liste = requests.get(args[0], headers=headers).json()

    result = tri_rendez_vous(liste)

except Exception as e:
    None
