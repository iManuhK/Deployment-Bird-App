# app.py

import os

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Bird

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Birds(Resource):

    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)
    
    def post(self):
        new_post = Bird(
            name = request.json.get['name'],
            species = request.json.get['species'],
        )

        db.session.add(new_post)
        db.session.commit()

        new_post_dict = new_post.to_dict()

        return make_response(new_post_dict, 201)

api.add_resource(Birds, '/birds')

class BirdByID(Resource):
    def get(self, id):
        bird = Bird.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(bird), 200)

api.add_resource(BirdByID, '/birds/<int:id>')
