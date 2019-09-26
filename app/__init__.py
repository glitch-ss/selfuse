from flask import Flask

app = Flask(__name__)
from app.process import views
from app.monitor import m_views
