from flask import Flask, render_template
from string import digits, ascii_lowercase
from random import sample
from yandi.views.authenticate import login_check, authenticate
from yandi.views.index import index
from yandi.views.vul_scanner import vul_scanner
from yandi.views.asset_management import asset_management
from yandi.views.plugin_management import plugin_management
from yandi.views.settings import settings
from yandi.views.dashboard import dashboard
from yandi.views.port_scanner import port_scanner
from yandi.views.subdomain_brute import subdomain_brute
from yandi.views.acunetix_scanner import acunetix_scanner
from yandi.views.auth_tester import auth_tester
from yandi.views.github_brute import github_brute
from yandi.views.todo import todo
from yandi.views.email_brute import email_brute
from yandi.views.log import log


app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join(sample(digits + ascii_lowercase, 10))

app.register_blueprint(authenticate)
app.register_blueprint(github_brute)
app.register_blueprint(email_brute)
app.register_blueprint(index)
app.register_blueprint(log)
app.register_blueprint(vul_scanner)
app.register_blueprint(asset_management)
app.register_blueprint(plugin_management)
app.register_blueprint(settings)
app.register_blueprint(todo)
app.register_blueprint(dashboard)
app.register_blueprint(port_scanner)
app.register_blueprint(subdomain_brute)
app.register_blueprint(acunetix_scanner)
app.register_blueprint(auth_tester)


@app.errorhandler(404)
@login_check
def page_not_fount(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
@login_check
def internal_server_error(e):
    return render_template('500.html'), 500
