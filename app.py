import datetime
import logging
import traceback

from flask import Flask, jsonify, request

from db import db
from models import Player

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///footballers"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@app.route('/')
def main_page():
    return "<html><head></head><body>A simple REST API for football players</a>.</body></html>"


@app.route('/players', methods=['POST'])
def create_player():
    try:
        r = request.get_json()
        r['last_modified'] = str(datetime.datetime.now())
        player = Player(**r)
        db.session.add(player)
        db.session.commit()
        return jsonify({'player': player.serialize}), 201
    except(TypeError):
        logging.info(traceback.print_exc())
        return exc_mess("Invalid input data."), 404
    except:
        logging.info(traceback.print_exc())
        return exc_mess("Player already exists."), 409


@app.route('/players/<id>', methods=["GET"])
def show_player(id):
    try:
        player = Player.query.filter_by(id=id).first()
        return jsonify(player.serialize)
    except:
        logging.info(traceback.print_exc())
        return exc_mess("Player does not exist"), 404


@app.route('/players/list/', methods=["GET"])
def show_player_list():
    try:
        players = [p for p in Player.query.all()]
        return jsonify({'players': [p.serialize for p in players]})
    except:
        logging.info(traceback.print_exc())
        return exc_mess("Players do not exist"), 404


@app.route('/players/<id>', methods=['PUT'])
def update_player(id):
    try:
        Player.query.filter_by(id=id).update(request.get_json())
        player = Player.query.filter_by(id=id).first()
        player.last_modified = str(datetime.datetime.now()).split('.')[0]
        db.session.commit()
        return jsonify({'player': player.serialize}), 201
    except:
        logging.info(traceback.print_exc())
        return exc_mess("Player does not exist"), 404


@app.route('/players/<id>', methods=["DELETE"])
def delete_player(id):
    try:
        Player.query.filter_by(id=id).delete()
        db.session.commit()
        return 'deleted'
    except:
        logging.info(traceback.print_exc())
        return exc_mess("Player does not exist."), 404


def exc_mess(message):
    response = jsonify({'error': message})
    traceback.print_exc()
    return response
