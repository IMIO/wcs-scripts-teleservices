import sys
try:
    #python3.4
    from importlib import reload
except:
    pass

sys.path.insert(0, "/var/lib/wcs/scripts")
sys.path.insert(0, "/var/lib/wcs-au-quotidien/scripts")
import dest

reload(dest)
result = "%(complement_adresse)s" % dest.get(globals())
