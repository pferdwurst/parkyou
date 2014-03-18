import datetime
from flask import url_for
from parkyou import db


# {
#   "_id" : ObjectId("53236de93e5d64590ce0c9f9"),
#     "created_at" : ISODate("2014-03-14T17:00:24.045Z"),
#     "objectid" : "sdf",
#     "sg_order_n" : "sdf",
#     "borough" : "B",
#     "desc" : "sdf",
#     "point" : {
#     "type" : "Point",
#         "coordinates" : [
#             -73.88606545610027,
#             40.81227304685457
#         ]
#     }
# }
#
#  
#
# > use parku
#    switched to db parku
# > show collections
#    feature
#    parking_sign
#    system.indexes
# > show feature
# > db.feature.find( { sg_order_n: "P-158196" })
# { "_id" : ObjectId("532371053e5d645b8d4b7c71"), "created_at" : ISODate("2014-03-14T17:13:41.404Z"), "objectid" : NumberLong(4168596), "sg_order_n" : "P-158196", "borough" : "B", "desc" : "NO PARKING (SANITATION BROOM SYMBOL) 11:30AM TO 1PM TUES & FRI <---->", "point" : { "type" : "Point", "coordinates" : [  -73.92242681624741,  40.82991920377618 ] } }



class Feature(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    objectid = db.LongField()
    sg_order_n = db.StringField(max_length=255, required=True)
    borough = db.StringField(required=True)
    desc = db.StringField(required = True)
    side = db.StringField()
    on_street = db.StringField()
    to_street = db.StringField()
    from_street = db.StringField()
    point = db.PointField(required = True)

    def __unicode__(self):
        return self.sg_order_n
    
    def latitude(self):
        return self.point["coordinates"][1]
    
    def longnitude(self):
        return self.point["coordinates"][0]
    

