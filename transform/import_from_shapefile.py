import shapefile

def records(filename):

# generator

reader = shapefile.Reader(filename)

fields = reader.fields[1:]

field_names = [field[0] for field in fields]

for sr in reader.shapeRecords():

geom = sr.shape.__geo_interface__

atr = dict(zip(field_names, sr.record))

yield dict(geometry=geom,properties=atr)

a = records('point.shp')
