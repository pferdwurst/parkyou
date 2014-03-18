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

def get_polylines():
     polylines = []
     regs = dbops.find_all_regulations()
     for reg in regs:
         signs = dbops.find_signs_for_regulation(reg)
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
@nocache
def show_map():
    latitude = 40.776366
    longitude =  -73.943280
    zoom = 14
    regs = get_polylines()
    
    return render_template("nyc.html", API_KEY = app.config["GOOGLE_MAP_KEY"], LAT = latitude, LONG = longitude, ZOOM = zoom, js = url_for('static', filename='polyline.js'), regulations = regs )


if __name__ == '__main__':
    app.run()

