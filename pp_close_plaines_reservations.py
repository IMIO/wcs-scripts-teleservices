import random
import requests, base64, hmac, hashlib, datetime
import time
import urllib
import urlparse

from hashlib import sha256
from wcs.formdef import FormDef


def sign_url(url, key, algo='sha256', orig=None, timestamp=None, nonce=None):
    parsed = urlparse.urlparse(url)
    new_query = sign_query(parsed.query, key, algo, orig, timestamp, nonce)
    return urlparse.urlunparse(parsed[:4] + (new_query,) + parsed[5:])

def sign_query(query, key, algo='sha256', orig=None, timestamp=None, nonce=None):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()
    timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
    if nonce is None:
        nonce = hex(random.getrandbits(128))[2:-1]
    new_query = query
    if new_query:
        new_query += '&'
    new_query += urllib.urlencode((
        ('algo', algo),
        ('timestamp', timestamp),
        ('nonce', nonce)))
    if orig is not None:
        new_query += '&' + urllib.urlencode({'orig': orig})
    signature = base64.b64encode(sign_string(new_query, key, algo=algo))
    new_query += '&' + urllib.urlencode({'signature':signature})
    return new_query

def sign_string(s, key, algo='sha256', timedelta=30):
    digestmod = getattr(hashlib, algo)
    hash = hmac.HMAC(key, digestmod=digestmod, msg=s)
    return hash.digest()

def close_plaines_reservation(context):
    first_date_other_demand = None
    last_date_other_demand = None
    cpt = 0
    demarches_closed = []
    for formdef in FormDef.select(lambda x: x.url_name=="aes-inscrire-mon-enfant-a-une-plaine"):
        option_first_date = formdef.workflow_options.get("first_date_plain")
        option_last_date = formdef.workflow_options.get("last_date_plain")
        for formdata in formdef.data_class().select(lambda y: y.user_id == str(context.get("form_user").id)):
            for field in formdef.get_all_fields(): # les autres champs
                if not hasattr(field, 'get_view_value'): # sauf les titres, etc.
                    continue
                if field.varname == "reg_first_date_plaine":
                    first_date_other_demand = formdata.get_field_view_value(field) or option_first_date
                if field.varname == "reg_last_date_plaine":
                    last_date_other_demand = formdata.get_field_view_value(field) or option_last_date
            if(context.get("form_var_reg_first_date_plaine") == first_date_other_demand and context.get("form_var_reg_last_date_plaine") == last_date_other_demand):
                url = "{}/portail-parent/aes-inscrire-mon-enfant-a-une-plaine/{}/jump/trigger/cloture".format(context.get("site_url"), formdata.id)
                url = sign_url(url, "d3c18cf7354042661b0cd20ebd9b628b6c021b9b6c3dcd186df5780889798bfb", orig="montsaintguibert-formulaires.guichet-citoyen.be")
                # print ("{} {} - {} {}".format(first_date, first_date_other_demand, last_date, last_date_other_demand))
                requests.post(url)
                demarches_closed.append(str(formdata.id))
    return ",".join(demarches_closed)


result = close_plaines_reservation(vars())
