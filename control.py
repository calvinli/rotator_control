from flask import Flask, request, render_template, jsonify

import tracker
import rot2prog

app = Flask(__name__)

@app.route('/')
def main_page():
    # this is waayyy too slow
    #az, el = rot2prog.get_pos()
    az, el = "?", "?"
    moon = tracker.get_moon_params()
    return render_template("index.html", az=az, el=el, moon_info=moon)

@app.route('/api/moon_info')
def moon_info():
    """Get some relevant current info about the moon."""
    return jsonify(tracker.get_moon_params())

@app.route('/api/get_pos')
def get_pos():
    """Get the current azimuth and elevation of the rotator."""
    try:
        az, el = rot2prog.get_pos()
        return jsonify({'az': az, 'el': el})
    except:
        return jsonify({'error': 'error'}), 500

@app.route('/api/set_pos', methods=['POST'])
def set_pos():
    """Set the rotator to the given azimuth and elevation.

    POST only.

    (Exit code 0 means the command was sent to the controller.
    It does not mean the rotator was actually set to the values given.)
    """
    try:
        az = int(request.form['az'])
        el = int(request.form['el'])
    except:
        return jsonify({'error': 'error'}), 400 # bad input
    
    try:
        return jsonify({'exit_code': rot2prog.set_pos(az, el)})
    except:
        return jsonify({'error': 'error'}), 500

@app.route('/api/set_to_moon', methods=['POST'])
def set_to_moon():
    az, el = tracker.sanitize_az_el(*tracker.get_moon_az_el())
    try:
        return jsonify({'exit_code': rot2prog.set_pos(az, el)})
    except:
        return jsonify({'error': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
