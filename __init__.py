from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask import render_template, url_for, redirect


from flask import make_response
from functools import update_wrapper

app = Flask(__name__)

# app.config.from_object('parkyou.default_settings')
# $ export PARKYOU_SETTINGS=conf/settings.cfg
app.config.from_envvar('PARKYOU_SETTINGS')


app.config["MONGODB_SETTINGS"] = {'DB': "parku"}


db = MongoEngine(app)

from parkyou.data import dbops
import json

# The center of the map will be Times Square
TS_LATITUDE = 40.759060
TS_LONGNITUDE = -73.984776
RADIUS = 1 # not sure what the unit on this is 

def get_polylines():
     polylines = []
     regs = dbops.find_all_regulations((TS_LONGNITUDE ,  TS_LATITUDE), RADIUS)
     for reg in regs:
         signs = dbops.find_signs_for_regulation(reg.sg_order_n)
         polylines.append(signs)
         
     return polylines


def nocache(f):
    def new_func(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp
    return update_wrapper(new_func, f)


@app.route('/')
@app.route('/index')
def index():
    return "Happy Parking!"


@app.route('/map')
@app.route('/map/')
@nocache
def show_map():
    regs = get_polylines()
    zoom = 17
    print "Found %d lines " % len(regs)
    return render_template("nyc.html", API_KEY = app.config["GOOGLE_MAP_KEY"], LAT = TS_LATITUDE, LONG = TS_LONGNITUDE, ZOOM = zoom, js = url_for('static', filename='polyline.js'), regulations = regs )


if __name__ == '__main__':
    app.run()

