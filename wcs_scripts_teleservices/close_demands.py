# Scripts for map statement management:
# close_demands.py
# has_close_demands.py
# similar_list.py
# similar_map.py

from pyproj import Proj, transform, Geod

from wcs.qommon import misc
from wcs.qommon.storage import Contains
from wcs.wf.geolocate import GeolocateWorkflowStatusItem

geod = Geod(ellps="WGS84")


def get_coords(context):
    coords = context.get("form_var_carte")
    if "form_var_numero" in context:
        geolocate = GeolocateWorkflowStatusItem()
        geolocate.method = "address_string"
        geolocate.address_string = (
            "{{ form_var_numero}} {{ form_var_voie }}, {{ form_var_commune }}, Belgique"
        )
        return geolocate.geolocate_address_string(None)
    if "form_var_voie" in context:
        geolocate = GeolocateWorkflowStatusItem()
        geolocate.method = "address_string"
        geolocate.address_string = (
            "{{ form_var_voie }}, {{ form_var_commune }}, Belgique"
        )
        return geolocate.geolocate_address_string(None)
    if coords:
        lat, lon = coords.split(";")
        return {"lat": float(lat), "lon": float(lon)}
    return None


def get_close_demands(formdef, coords, context):
    applied_filters = [
        "wf-%s" % x.id for x in formdef.workflow.get_not_endpoint_status()
    ]
    formdatas = formdef.data_class().select([Contains("status", applied_filters)])
    counter = 0
    for formdata in formdatas:
        structured_item = formdata.get_as_dict()
        if (
            "var_first_observation" in structured_item.keys()
            and structured_item["var_first_observation"] != "True"
        ):
            continue
        if not formdata.geolocations:
            continue
        formdata_coords = misc.normalize_geolocation(formdata.geolocations["base"])

        distance = geod.inv(
            formdata_coords["lon"], formdata_coords["lat"], coords["lon"], coords["lat"]
        )[2]
        formdata._distance = distance
        formdata._coords = formdata_coords
        if context is not None:
            zoom_max = context.get("form_option_zoom_max") or "750"
        else:
            zoom_max = "750"
        if distance < int(zoom_max):
            counter += 1
            formdata.counter = counter
            yield formdata


if __name__ in ("__builtins__") and "form_objects" in vars():
    coords = get_coords(vars())
    if coords or True:
        result = get_close_demands(form_objects.formdef, coords, vars())
