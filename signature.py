import random
import base64
import datetime
import hashlib
import hmac
import urllib.parse
import requests


def sign_url(
    url,
    key,
    algo="sha256",
    orig=None,
    timestamp=None,
    nonce=None,
    nameid=None,
):
    parsed = urllib.parse.urlparse(url)
    new_query = sign_query(parsed.query, key, algo, orig, timestamp, nonce, nameid)
    return urllib.parse.urlunparse(parsed[:4] + (new_query,) + parsed[5:])


def sign_query(
    query,
    key,
    algo="sha256",
    orig=None,
    timestamp=None,
    nonce=None,
    nameid=None,
):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow()
    timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    new_query = query
    if new_query:
        new_query += "&"
    new_query += urllib.parse.urlencode(
        (("algo", algo), ("timestamp", timestamp), ("nonce", nonce), ("NameID", nameid))
    )
    if orig is not None:
        new_query += "&" + urllib.parse.urlencode({"orig": orig})
    signature = base64.b64encode(sign_string(new_query, key, algo=algo))
    new_query += "&" + urllib.parse.urlencode({"signature": signature})
    return new_query


def sign_string(s, key, algo="sha256", timedelta=30):
    if not isinstance(key, bytes):
        key = key.encode("utf-8")
    if not isinstance(s, bytes):
        s = s.encode("utf-8")
    digestmod = getattr(hashlib, algo)
    hash = hmac.HMAC(key, digestmod=digestmod, msg=s)
    return hash.digest()

try:

    # Clé d’accès de l'appel webservice
    api_access_key = None if args[0] == "" else args[0]
    # identifiant d'accès de l'api
    api_ident = None if args[1] == "" else args[1]
    # uuid d'un utilisateur ayant accès à ce qu'on demande (admin)
    api_user_nameid = None if args[2] == "" else args[2]
    api_generated_nonce = hex(random.getrandbits(128))[2:].rstrip("L")
    # L'url de ce qu'on veut pepom
    publik_url = args[3]

    url = sign_url(
        publik_url,
        api_access_key,
        orig=api_ident,
        nameid=api_user_nameid,
        nonce=api_generated_nonce,
    )

    result = url

except Exception as e:
    result = str(e)
