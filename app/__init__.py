
from flask import Flask
import os

app = Flask(__name__)
from app import routes
app.config.update({'SECRET_KEY': os.environ.get('SECRET_KEY')})
app.register_blueprint(routes.bp)
