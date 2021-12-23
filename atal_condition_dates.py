import datetime
import time


indisponibilites_salles = args[0]

date_debut_demande = args[1]
date_fin_demande = args[2]
heure_debut_demande = args[3]
heure_fin_demande = args[4]

date_debut_demande = datetime.date(int(date_debut_demande.split("/")[2]), int(date_debut_demande.split("/")[1]), int(date_debut_demande.split("/")[0]))
date_fin_demande = datetime.date(int(date_fin_demande.split("/")[2]), int(date_fin_demande.split("/")[1]), int(date_fin_demande.split("/")[0]))
heure_debut_demande = time.strptime(heure_debut_demande, "%H:%M")
heure_debut_demande = datetime.time(heure_debut_demande.tm_hour, heure_debut_demande.tm_min)
heure_fin_demande = time.strptime(heure_fin_demande, "%H:%M")
heure_fin_demande = datetime.time(heure_fin_demande.tm_hour, heure_fin_demande.tm_min)

datetime_debut_demande = datetime.datetime.combine(date_debut_demande, heure_debut_demande)
datetime_fin_demande = datetime.datetime.combine(date_fin_demande, heure_fin_demande)

format_date = "%Y-%m-%dT%H:%M"

for indisponibilite in indisponibilites_salles:
    debut_location = datetime.datetime.strptime(indisponibilite["StartDate"][:16], format_date)
    fin_location = datetime.datetime.strptime(indisponibilite["EndDate"][:16], format_date)
    if debut_location < datetime_debut_demande < fin_location or debut_location < datetime_fin_demande < fin_location:
        result = False

result = True
