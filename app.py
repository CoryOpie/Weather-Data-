from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
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
def home():
    return (f"Available Routes<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/startdate<br/>"
            f"/api/v1.0/startdate/enddate<br/>"
            f"Start and end date should be in 'YYYY-MM-DD' format"

    )

#Convert query results to dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_data = session.query(measurement.date, measurement.prcp).all()
    dict_prcp = dict(prcp_data)
    session.close()
    return jsonify(dict_prcp)


#Return a JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(station.station).all()
    session.close()
    return jsonify(stations)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date = last_date[0]
    year, month, day = map(int, last_date.split("-"))
    year_ago = dt.date(year, month, day) - dt.timedelta(days=365)
    year_ago = (year_ago.strftime("%Y-%m-%d"))
    tobs = session.query(measurement.date, measurement.tobs).all()
    session.close()
    return jsonify(tobs)

# .filter(measurement.date >= year_ago)

#start only calc
@app.route("/api/v1.0/<start>")
def start_date(start):
    list = []
    session = Session(engine)
    temp = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()
    for data in temp:
        dict = {}
        dict["Tmin"] = data[0]
        dict["Tavg"] = round(data[1],1)
        dict["Tmax"] = data[2]
        list.append(dict)


    return jsonify(list)



#start and end

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    list=[]
    session = Session(engine)

    temp = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).group_by(measurement.date).all()

    session.close()
    for data in temp:
        dict = {}
        dict["Date"] = data[0]
        dict["Tmin"] = data[1]
        dict["Tavg"] = round(data[2],2)
        dict["Tmax"] = data[3]
        list.append(dict)


    return jsonify(list)



if __name__ == "__main__":
    app.run(debug=True)




