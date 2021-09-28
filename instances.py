import redis as redis
from flask import Flask

app = Flask(__name__)
redis = redis.Redis(host='127.0.0.1')