from flask import Flask
from flask import request, jsonify
import datetime as dt
import numpy as np
import pandas as pd
from pandas import DataFrame
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect	
app = Flask(__name__)
app.debug=True
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base() 
# reflect the tables
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
def getPrecipitationData():
	busy_station = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).\
               order_by(func.count(Measurement.tobs).desc()).all()

	busiest = busy_station[0][0] 
	
	temperature = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == busiest).\
    filter(Measurement.date > "2016-08-23").\
    order_by(Measurement.date).all()
	adate = dt.datetime.today().strftime('%Y-%m-%d')
	aaa = {}
	for k in temperature:
		aaa[k[1]] = k[2]
	#end of my program and returning a value--------------------
	return(jsonify(aaa))
	
def getStationData():
	busy_station1 = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).\
               order_by(func.count(Measurement.tobs).desc()).all()
	return(jsonify(busy_station1))

def displayTOBS():
	return ("Displaying TOBS")
@app.route('/')
@app.route('/hello')
def api():
    return ("This is my API route")

@app.route('/api/v1.0/precipitation')
def api2():
	return (getPrecipitationData())

@app.route('/api/v1.0/stations')
def api3():
	return (getStationData())
	
@app.route('/api/v1.0/tobs')
def api4():
	return (displayTOBS())

app.run()