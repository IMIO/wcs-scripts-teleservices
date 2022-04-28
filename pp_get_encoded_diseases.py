# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, '/var/lib/wcs/scripts')
sys.path.insert(0, '/var/lib/wcs-au-quotidien/scripts')

def get_disease_from_index (data_source, diseases, other_diseases, index):
    # set empty list if parameters are None
    if diseases is None:
        diseases = []
    if other_diseases is None:
        other_diseases = []

    # cast index into an integer
    index = int(index)

    # get the total length of the two list
    diseases_length = len(diseases or []) + len(other_diseases or [])

    # start process
    
    # if index is more than total of to list :
    # return None
    if index >= diseases_length:
        result = None
    
    # if index is less than length of first list,
    # get text from data source and return text
    elif index < len(diseases):
        result = [disease['text'] for disease in data_source if disease['id'] == diseases[index]][0]

    # if index is less than than total of two list     
    # adapt index to the second list and return the element
    elif index < diseases_length:
        index -= len(diseases)
        result = other_diseases[index][0]
    
    # return result
    return result or ''
 

if "args" in vars() and vars().get('args')[0] == "get_disease_from_index":
    if len(args) == 4:
        result = get_disease_from_index(data_source.aes_diseases, vars().get(args[1]), vars().get(args[2]), vars().get('args')[3])
    else:
        result = "Need 3 argument, " + str(len(args) - 1) + " given !"

