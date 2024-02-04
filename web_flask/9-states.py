#!/usr/bin/python3
"""
Starts a Flask web application.
The application listens on 0.0.0.0, port 5000.
"""
from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception=None):
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    return render_template('7-states_list.html', states=storage.all(State))


@app.route('/states/<id>', strict_slashes=False)
def cities_by_states(id):
    for state in storage.all(State).values():
        if id == state.id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
