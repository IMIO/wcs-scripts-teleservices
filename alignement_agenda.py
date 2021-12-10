import datetime
from datetime import date
from datetime import timedelta

import requests


def tri_rendez_vous(liste_creneaux, date_alignement):
    """
    :param liste_creneaux: liste dictionnaire des creneaux horaire
    :param date_alignement: datetime.datetime date à laquelle les créneaux horaire vont être disponible
    :return: liste du type de rendez-vous avec nombre de personne
    """
    return [x for x in liste_creneaux["data"] if date_alignement <= datetime.datetime.strptime(x["date"], "%Y-%m-%d")]


try:
    headers = {'Accept': 'application/json'}
    # args[0] == l'url des créneaux horaire
    # args[1] == le nombre de jour d'alignement
    liste_creneaux = requests.get(args[0], headers=headers).json()
    date_alignement = date.today() + timedelta(days=args[1])
    date_alignement = datetime.datetime.fromordinal(date_alignement.toordinal())
    result = tri_rendez_vous(liste_creneaux, date_alignement)
except Exception as e:
    None
