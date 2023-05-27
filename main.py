from flask import Flask, jsonify, Response
import os
from flask import Flask
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

fastf1.plotting.setup_mpl()

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
    app.run(debug=True, port=os.getenv("PORT", default=5000))
