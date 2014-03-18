from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "parku"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)


def get_polylines():
     polylines = []
     regs = dbops.find_all_regulations()
     for reg in regs:
         signs = dbops.find_signs_for_regulation(reg)
         polylines.append(signs)
     return polylines

if __name__ == '__main__':
    app.run()

