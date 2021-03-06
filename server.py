from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, BobaShop, connect_to_db, db

import googlemaps

from pprint import pformat
import os
import json

key = os.getenv("GOOGLE_PLACES_KEY")
print('key: ', key)

app = Flask(__name__)


app.secret_key = "wiggles"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/boba_map")
def find_bobashops():
    """Search for Boba Shops from Google Places nearbysearch & display list of shops"""

 #for now will just render map of current location
    return render_template("boba_map.html", key=os.getenv("GOOGLE_PLACES_KEY"))




@app.route("/registration_form", methods=["GET", "POST"])
def register_process():
	"""Registration form and process"""

	if request.method == "GET":
		return render_template("registration_form.html")

	else:
		email = request.form.get("email")
		password = request.form.get("password")

		if not User.query.filter(User.email == email).first():
			user = User(email=email, password=password)
			db.session.add(user)
			db.session.commit()
			return redirect("/")
		else:
			flash('An account with that email already exists!')
			return render_template("registration_form.html")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(port=5000, host='0.0.0.0')
