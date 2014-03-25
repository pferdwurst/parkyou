import os, sys
import csv
from pprint import pprint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from parkyou.models import *

import mongoengine

# Locations.csv e.g.
#
#   B,P-010938,WOOD AVENUE,METROPOLITAN AVENUE,WEST AVENUE,S
#   B,P-049703,BECK STREET,WESTCHESTER SQUARE,KIRK STREET,W


# Fields:
#    borough
#    sg_order_n
#    on_street
#    from_street
#    to_street
#    side


def import_locations():
    LOCATIONS_CSV="locations.CSV"
    
    LIMIT = 100
    
    count = 0
    
    with open(LOCATIONS_CSV, "rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        
        for row in csvreader:
            if count > LIMIT:
                break
            (borough, sign, on_street, from_street, to_street, side) = row
            try:
                print "Updating %s" % sign
                Feature.objects(sg_order_n = sign).update(upsert = True, set__on_street = on_street,
                                                                         set__from_street = from_street,
                                                                         set__to_street = to_street,
                                                                         set__side = side,
                                                                         set__borough = borough)
                
                count += 1
            except mongoengine.errors.OperationError as error:
                print "Cannot update %s: %s" % (sign , error)
            
#
# signs.CSV
#  B,P-004958,2,0009 ,   ,Property Line
#  B,P-004958,3,0030 ,   ,NIGHT REGULATION (MOON & STARS SYMBOLS) NO PARKING (SANITATION BROOM SYMBOL) MIDNIGHT TO 3AM TUES & FRI <--> (SUPERSEDED BY SP-841C)                                    
#  B,P-004958,4,0030 ,   ,1 HOUR PARKING 9AM-7PM EXCEPT SUNDAY (SUPERSEDED BY PS-55CB)   

def import_signs():
    SIGNS_CSV="signs.CSV"
    
    LIMIT = 100
    count = 0
    
    with open(SIGNS_CSV, "rb") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            if count > LIMIT:
                break
            
            (borough, sign, order, feet, side, desc) = row
               
            try:
               print "Updating %s" % sign
               Feature.objects(sg_order_n = sign, desc = desc).update(upsert = True, set__order = order,
                                                                                     set__feet = feet_from_intersection)
               count += 1
            except mongoengine.errors.OperationError as error:
                print "Cannot update %s: %s" % (sign , error)
            

if __name__ == '__main__':
    
    import_signs()