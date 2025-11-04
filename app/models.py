from app import db
from datetime import datetime
from . import login_manager
from flask_login import UserMixin

favorites = db.Table('favorites', db.Column('user_id', db.Integer, db.ForeignKey('user.id')), db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')))

class Recipe(db.Model): #Recipe created by user
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80)) #max length 80 characters
    description = db.Column(db.Text) #text box
    ingredients = db.Column(db.Text) #text box
    instructions = db.Column(db.Text) #text box
    date = db.Column(db.DateTime)
    tags = db.Column(db.String(200)) # tags with commas

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='recipes')
    ratings = db.relationship('Rating', backref='rated_recipe', cascade="all, delete-orphan") #relationship with rating
    comments = db.relationship('Comment', backref='commented_recipe', cascade="all, delete-orphan") #relationship with comment

class User(db.Model, UserMixin): #Account info
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique = True , nullable = False) #max length 32 characters
    email = db.Column(db.String(100), unique = True , nullable = False) #max length 100 characters
    password = db.Column(db.String(32), nullable = False) #max length 32 characters
    comments = db.relationship('Comment', backref='user') #relationship with comment
    ratings = db.relationship('Rating', backref='user')
    favorites = db.relationship('Recipe', secondary=favorites, backref='favoriters')

class Comment (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete='CASCADE'), nullable=False)
    recipe = db.relationship('Recipe', backref="specific_comment")

class Rating (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete='CASCADE'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))

