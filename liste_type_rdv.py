import requests
import json


def tri_rendez_vous(liste, variable):
    """
    :param liste: liste json des types de rendez-vous
    :param variable: str type de rendez-vous sélectionné
    :return: liste du type de rendez-vous avec nombre de personne
    """
    return set([x for x in liste["data"] if variable in x["text"]])


try:
    headers = {'Accept': 'application/json'}
    # args[0] == l'url des types de rendez-vous
    # args[1] == le type de rendez-vous sélectionné
    liste = requests.get(args[0], headers=headers).json()
    result = tri_rendez_vous(liste, args[1])
except Exception as e:
    None
