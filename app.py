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

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")
        
@app.route("/api/v1.0/precipitation")

def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
#Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    # Query all passengers
    sel = [Measurement.prcp,Measurement.date]
    results = session.query(*sel).\
    filter(Measurement.date > '2016-08-23').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_precipitation = []
    for prcp, date in results:
        precip_dict = {}
        precip_dict["Precip"] = prcp
        precip_dict["Date"] = date
        all_precipitation.append(precip_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")

def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

#Return a JSON list of stations from the dataset
    results2=session.query(func.distinct(Measurement.station)).all()

    session.close()

    # Convert list of tuples into normal list
    station = list(np.ravel(results2))

    return jsonify(station)


@app.route("/api/v1.0/tobs")

def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

#Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    # Query all passengers
    sel = [Measurement.station, 
    func.max(Measurement.tobs), 
    func.min(Measurement.tobs), 
    func.avg(Measurement.tobs),
    func.count(Measurement.station)]
    results1 = session.query(*sel).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(results1))

    return jsonify(tobs)

# @app.route("/api/v1.0/<start>")
# def 

# @app.route("/api/v1.0/<start>/<end>")
# def 

if __name__ == '__main__':
    app.run(debug=True)