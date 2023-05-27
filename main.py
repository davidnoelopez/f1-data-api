import io

import fastf1
import fastf1.plotting
from flask import Flask, Response, jsonify, request
from flask_pymongo import PyMongo
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import bson.json_util as json_util

app = Flask(__name__)
app.config.from_object('config.Config')
mongo = PyMongo(app, uri=app.config["MONGO_URI"])
print("Connected to MongoDB")
db = mongo.db

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Checo app 🚅"})

@app.route("/api/driver/", methods=["POST", "GET"])
def create_driver():
    if  request.method == "POST":
        data = request.form
        driver = {
            "name": data["name"],
            "team": data["team"],
            "number": data["number"]
        }

        if db is not None:
            db.drivers.insert_one(driver)
            return json_util.dumps(driver) , 201
        else:
            return jsonify({"message": "No database connection"}), 500

    else:
        drivers = "TEST"
        return jsonify({"drivers": drivers})


@app.route("/api/lap_plot")
def lap_plot():
    session = fastf1.get_session(2019, 'Monza', 'Q')

    session.load()
    fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
    lec_car_data = fast_leclerc.get_car_data()
    t = lec_car_data['Time']
    vCar = lec_car_data['Speed']

    # Plot the data

    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Speed (km/h)')
    ax.set_title('Leclerc fastest lap at Monza 2019')
    ax.plot(t, vCar)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"])
