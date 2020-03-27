from datetime import datetime

# Test with : python pp_get_dates_from_week_number.py
DEBUG = False

jours = {"Monday":"Lundi",
        "Tuesday":"Mardi",
        "Wednesday":"Mercredi",
        "Thursday":"Jeudi",
        "Friday":"Vendredi",
        "Saturday":"Samedi",
        "Sunday":"Dimanche"
        }

def find_week(lst_days):
    return True if WEEK in lst_days else False

def trad(str_date):
    for k,v in jours.items():
        str_date = str_date.replace(k,v)
    return str_date

def get_dates_from_week_number(context):
    lst_days = context.get("form_var_days_will_be_filtering")
    keep_days = list(filter(find_week, lst_days))
    dt_lst_days = []
    for day in keep_days:
        dt_day = datetime.strptime(day.split("_")[1], "%d/%m/%Y")
        dt_lst_days.append(dt_day)
    dt_lst_days.sort()
    str_firstday = trad(dt_lst_days[0].strftime("%A %d/%m/%Y"))
    str_lastday = trad(dt_lst_days[-1].strftime("%A %d/%m/%Y"))
    return [str_firstday, str_lastday]

if DEBUG is True:
    # sample
    form_var_current_validating_week = "s35"
    form_var_days_will_be_filtering = ['S35_25/08/2020', 'S35_28/08/2020', 'S35_26/08/2020', 'S35_27/08/2020', 'S35_24/08/2020']

CONTEXT = vars()
WEEK = CONTEXT.get("form_var_current_validating_week","").upper()
result = get_dates_from_week_number(CONTEXT)

if DEBUG is True:
    print result
