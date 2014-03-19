import shapefile
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from parkyou.models import *

FILE = "Parking_Regulation_Shapefile/Parking_Regulation_WSG84_March2014.shp"

def records(filename):

    # generator
    reader = shapefile.Reader(filename)

    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    
    
    for sr in reader.shapeRecords():
       geom = sr.shape.__geo_interface__
       atr = dict(zip(field_names, sr.record))
       yield dict(geometry=geom, properties=atr)


print "Importing from %s " % FILE
a = records(FILE)

count = 0
for _ in range(2000):
    feat = a.next()
#for feat in a:
    f = Feature(
                sg_order_n=feat["properties"]["SG_ORDER_N"],
                desc=feat["properties"]["SIGNDESC1"],
                object_id=feat["properties"]["OBJECTID"],
                point=feat["geometry"],
                borough="UNKNOWN"
                )
    print "Inserting %s " % feat["properties"]["OBJECTID"]
    f.save()
    count += 1
        
print "Inserted %d records. " % count
    


# B - Bronx
# K - Brooklyn, Kings County
# M - Manhattan
# Q - Queens
# S - Staten Is.
