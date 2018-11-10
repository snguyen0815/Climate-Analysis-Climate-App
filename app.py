############################

User: Stanley Nguyen

############################


import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def rain():
    
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-01-03', Measurement.date <= '2017-01-03').all()

    rec = list(np.ravel(precipitation))

    return jsonify(rec)

@app.route("/api/v1.0/stations")  
def station():

    station = session.query(Station.station).all()

    rec = list(np.ravel(station))

    return jsonify(rec)


@app.route("/api/v1.0/tobs")
def tobs():

    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between('2016-01-03','2017-01-03')).\
        order_by(Measurement.date).all()

    rec = list(np.ravel(tobs))

    return jsonify(rec)

@app.route("/api/v1.0/<start_date>")
def calc_start_climateTemp(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    climateTemp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    rec = list(np.ravel(climateTemp))

    return jsonify(rec)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_climateTemp(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    climateTemp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    rec = list(np.ravel(climateTemp))

    return jsonify(rec)
   
if __name__ == '__main__':
    app.run(debug=True)