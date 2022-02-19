from flask import Blueprint, jsonify, request
from flask_login import login_required
from marvel_inventory.helpers import token_required
from marvel_inventory.models import db, User, Character, character_schema, characters_schema
from datetime import datetime

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return jsonify({'some': 'value'})


# create character Route
@api.route('/characters', methods=['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    description = request.json['description']
    comics_appeared = request.json['comics_appeared']
    super_power = request.json['super_power']
    date_created = str(datetime.utcnow)
    user_token = current_user_token.token 

    character = Character(name, description, comics_appeared, super_power, date_created, user_token)
    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# retrieve ALL character
@api.route('/characters', methods=['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.query.filter_by(user_token = owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)


# retrieve a single character
@api.route('/character/<id>', methods=['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token.token
    character = Character.query.get(id)
    response = character_schema.dump(character)
    return jsonify(response)

@api.route('/characters/<id>', methods=['POST','PUT'])
@token_required
def update_character(current_user_token, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.description = request.json['description']
    character.comics_appeared = request.json['comics_appeared']
    character.super_power = request.json['super_power']
    character.date_created = request.json['date_created']
    character.user_token = current_user_token.token 

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

@api.route('/characters/<id>', methods=['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)