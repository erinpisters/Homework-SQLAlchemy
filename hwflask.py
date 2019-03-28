import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        f"<p>Welcome to the Hawaii Weather API Page</p>"
        f"<p>Available Routes:</p>"
        f"/api/v1.0/precipitation <br/> Returns a JSON list of precipitation data between the dates of 8/23/16 to 8/23/17<br/><br/>"
        f"/api/v1.0/stations<br/> Returns a JSON list of weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/> Returns a JSON list of Temperature Observations (tobs) for the previous year<br/><br/>"
        f"/api/v1.0/<start><br/> Reutrns a JSON list of min, avg, and max temperatures for all dates greater than and equal to the start date.<br/><br/>"
        f"/api/v1.0/<start>/<end><br/> Returns a JSON list of min, avg, and max temperatures for all dates between the start and end date inclusive<br/><br/>"

    )

#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    p_route = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date>=one_yr).group_by(Measurement.date).all()
    return jsonify(p_route)

#Station Route 
@app.route("/api/v1.0/stations")
def stations():
    s_route = session.query(Station.station, Station.name).all()
    return jsonify(s_route)

#Temperature Observation Route 
@app.route("/api/v1.0/tobs")
def tobs():
    t_route = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date <= one_yr).all()
    return jsonify(t_route)

#Start Date Only Route 
@app.route("/api/v1.0/<date>")
def StartDate():
    startd_route = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement >= date).all()
    return jsonify(startd_route)

#Start and End Date Route 
@app.route("/api/v1.0/<start>/<end>")
def StartEndDate():
    sed_route = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(sed_route)


if __name__ == "__main__"
    app.run(debug=True)