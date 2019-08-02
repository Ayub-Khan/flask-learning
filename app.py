""" Base App Config file """
import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# Init App
app = Flask(__name__)
base_directory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    base_directory,
    'db.sqlite'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)


class User(db.Model):
    """
    User Model for the Rest Apis
    """
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(marshmallow.Schema):
    """
    Defines Schema for User Model
    """
    class Meta:
        """
        Meta Class.
        """
        fields = ('first_name', 'last_name', 'username', 'password', 'email')


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)


@app.route('/user', methods=['GET'])
def get_all_users():
    """ Retuns all Users data. """
    users = User.query.all()
    serializer = users_schema.dump(users)
    return jsonify(serializer.data)


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    """ Retuns User data. """
    user = User.query.filter_by(username=username).first()
    return jsonify(user_schema.dump(user))


@app.route('/user', methods=['POST'])
def create_user():
    """ Creates a User. """
    data = request.get_json()
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'Status': 'New User Created.'
    })


@app.route('/user/<username>', methods=['PUT'])
def update_user(username):
    """ Updates User data. """
    data = request.get_json()
    user = User.query.filter_by(username=username).first()
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.user_name = data['username']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify({
        'Status': 'Updated User Data.'
    })


@app.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
    """ Deletes the User. """
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        'Status': 'User Deleted.'
    })


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
