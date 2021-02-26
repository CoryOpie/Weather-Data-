from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime, timedelta
from itertools import chain



engine = create_engine("sqlite:///Resources/hawaii.sqlite")


#reflect
Base = automap_base()

#reflect
Base.prepare(engine, reflect=True)

station = Base.classes.station
measurement = Base.classes.measurement

#####################
#      Flask        #
#####################
app = Flask(__name__)

#####################
#      Routes       #
#####################

#Home

@app.route("/")
def home()
    return (f""
    )











