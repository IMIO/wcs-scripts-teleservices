# Script pour vérifier que les dates encodées par l'utilisateur ne sont libre pour la location de la salle

import datetime
import time

# liste dict des indisponibilités de la salle
indisponibilites_salles = args[0]

date_debut_demande = args[1]
date_fin_demande = args[2]
heure_debut_demande = args[3]
heure_fin_demande = args[4]

# format string to date
date_debut_demande = datetime.date(int(date_debut_demande.split("/")[2]), int(date_debut_demande.split("/")[1]), int(date_debut_demande.split("/")[0]))
date_fin_demande = datetime.date(int(date_fin_demande.split("/")[2]), int(date_fin_demande.split("/")[1]), int(date_fin_demande.split("/")[0]))

# format string to time to datetime.time
heure_debut_demande = time.strptime(heure_debut_demande, "%H:%M")
heure_debut_demande = datetime.time(heure_debut_demande.tm_hour, heure_debut_demande.tm_min)
heure_fin_demande = time.strptime(heure_fin_demande, "%H:%M")
heure_fin_demande = datetime.time(heure_fin_demande.tm_hour, heure_fin_demande.tm_min)

# combine date and time to datetime
datetime_debut_demande = datetime.datetime.combine(date_debut_demande, heure_debut_demande)
datetime_fin_demande = datetime.datetime.combine(date_fin_demande, heure_fin_demande)

# string format for Atal datetime
format_date = "%Y-%m-%dT%H:%M"

# morceau de feuille
resultat = True

# parcours des indisponibilités si une date tombe en même temps que la date d'une demande retourne False
for indisponibilite in indisponibilites_salles:
    debut_location = datetime.datetime.strptime(indisponibilite["StartDate"][:16], format_date)
    fin_location = datetime.datetime.strptime(indisponibilite["EndDate"][:16], format_date)
    if debut_location < datetime_debut_demande < fin_location or debut_location < datetime_fin_demande < fin_location:
        resultat = False

result = resultat
