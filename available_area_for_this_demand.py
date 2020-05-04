# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')

if "args" in vars() and len(args) == 2:
    # args[0] is a datasource of administration's address and antenes
    # args[1] is a python-list
    # the result is the areas from the datasource if their id are in the python-list
    result = [area for area in args[0] if area['id'] in args[1]]
else:
    result = 'need 2 args'
