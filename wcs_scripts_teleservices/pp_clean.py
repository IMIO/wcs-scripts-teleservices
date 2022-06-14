# sudo -u wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=montsaintguibert-formulaires.guichet-citoyen.be pp_clean.py
# Clean all forms in Treatment!! (Not in kart)
from wcs.formdef import FormDef
for formdef in FormDef.select(lambda x: x.url_name=="aes-inscrire-mon-enfant-a-une-plaine"):
        formdef.data_class().wipe()
