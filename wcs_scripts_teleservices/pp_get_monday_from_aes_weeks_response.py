# This code return only monday and should be rewritten after summer 2021
# or maybe merged with pp_get_dates_from_week_number.py

from datetime import datetime


def get_monday_from_week_number(counter, weeks):
    week = weeks[counter].get('week')
    monday = datetime.strptime('1-{}-2021'.format(week), "%w-%W-%Y")
    return datetime.strftime(monday, "%d/%m/%Y")


result = get_monday_from_week_number(int(vars().get("form_var_aes_response_counter")),
                                     vars().get("form_var_activities_plaines_structured"))
