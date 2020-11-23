"""
Ce script sert à calculer le total à payer dans un bloc de champs ou un des éléments est une liste alimentée par une
source de données qui a une clef supplémentaire nommée 'price'.
"""

from decimal import Decimal

def total(fields_bloc):
    total = 0

    for field in fields_bloc:
        for value in field.values():
            if isinstance(value, dict):
                total += Decimal(value.get('price'))

    return total


try:
    result = total(args[0])
except:
    result = 'No input'