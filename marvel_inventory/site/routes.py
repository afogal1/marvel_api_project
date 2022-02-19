from flask import Blueprint, render_template
from flask_login import login_required


site = Blueprint('site', __name__, template_folder='site_templates')
"""
Note that in the above code some arguments are specified the Blueprint object
the first argument, 'site' is teh blueprints name
which is used by Flasks routing mechanism,
the second argument, __name__, is the Blueprints import name, 
which Flask uses to locate the Blueprints resource
"""

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')