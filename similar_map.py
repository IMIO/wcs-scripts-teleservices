# -*- coding: utf-8 -*-
# Scripts for map statement management:
# close_demands.py
# has_close_demands.py
# similar_list.py
# similar_map.py

import os
import sys

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

import json
import time

from wcs.qommon.form import MapWidget

import close_demands

result = ""
coords = close_demands.get_coords(vars())
incidents = {
    "Voie publique": "#7F7F7F",
    "Déchets - Propreté publique": "#674D24",
    "Avaloir - Taque": "#40A497",
    "Graffiti - Tag - Affichage sauvage": "#E423FF",
    "Espace vert": "#67B976",
    "Signalisation": "#FB9A01",
    "Eclairage public en panne ou qui clignote": "#ECEE6C",
    "Eclairage public": "#ECEE6C",
    "Signalisation": "#6CA3EE",
    "Dégradation du mobilier urbain": "#8F1E06",
}

if coords:
    map_widget = MapWidget(
        "geo", readonly=True, value="%(lat)s;%(lon)s" % coords, initial_zoom=16
    )
    formdef = form_objects.formdef

    features = []
    for formdata in close_demands.get_close_demands(formdef, coords, vars()):
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [formdata._coords["lon"], formdata._coords["lat"]],
            },
        }
        for field in formdef.fields:
            if field.varname in (
                "numero",
                "voie",
                "commune",
                "message",
                "type_probleme",
                "incident",
            ):
                feature["properties"][field.varname] = formdata.data.get(field.id)
                if field.varname == "incident":
                    feature["properties"]["color"] = incidents.get(
                        formdata.data.get(field.id)
                    )
        feature["properties"]["datetime"] = time.strftime(
            "%d/%m/%Y %H:%M", formdata.receipt_time
        )
        feature["properties"]["reference"] = "%s:%s" % (formdef.url_name, formdata.id)
        feature["properties"]["id"] = formdata.id
        feature["properties"]["counter"] = formdata.counter
        features.append(feature)

    result = """
       <link href="%s/static/css/combo.map.css" type="text/css" media="all" rel="stylesheet">
       <div id="similar"><script>geojson_data = %s;</script>%s</div>
    """ % (
        portal_user_url,
        json.dumps(features),
        map_widget.render(),
    )
