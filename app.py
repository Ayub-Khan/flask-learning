""" Base App Config file """
import os

from cryptography.fernet import Fernet
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import post_dump
from sqlalchemy.exc import IntegrityError

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
auth = HTTPBasicAuth()
ENABLE_ENCRIPTION = False
ENCRYPTION_KEY = b'qYEqBk7PxXgFN4A7_Nt6exidBY8qwUtrr88_Ful-enY='
encrptor = Fernet(ENCRYPTION_KEY)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return True


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

    def verify_password(self, password):
        return self.password == password


class UserSchema(marshmallow.Schema):
    """
    Defines Schema for User Model
    """
    class Meta:
        """
        Meta Class.
        """
        fields = ('first_name', 'last_name', 'username', 'password', 'email')

    def _encrypt_dict_data(self, single_user_data):
        if not ENABLE_ENCRIPTION:
            return single_user_data
        encrypted_dict = {}
        for key, value in single_user_data.items():
            encrypted_key = encrptor.encrypt(str(key).encode()).decode()
            encrypted_value = encrptor.encrypt(str(value).encode()).decode()
            encrypted_dict[encrypted_key] = encrypted_value
        return encrypted_dict

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            encrypted_data = []
            for user in data:
                encrypted_user_data = self._encrypt_dict_data(user)
                encrypted_data.append(encrypted_user_data)
            return encrypted_data
        encrypted_data = self._encrypt_dict_data(data)
        return encrypted_data


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)


def encrypted_status_response(message):
    """
    Helper method encrypts the status response.
    """
    if ENABLE_ENCRIPTION:
        return {
            encrptor.encrypt('status'.encode()).decode(): encrptor.encrypt(
                str(message).encode()).decode()
        }
    return {'status': message}


@app.route('/user', methods=['GET'])
@auth.login_required
def get_all_users():
    """ Retuns all Users data. """
    users = User.query.all()
    if users:
        serializer = users_schema.dump(users)
        return jsonify(serializer.data)
    return jsonify(encrypted_status_response('No user data available.'))


@app.route('/user/<username>', methods=['GET'])
@auth.login_required
def get_user(username):
    """ Retuns User data. """
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(user_schema.dump(user))
    return jsonify(encrypted_status_response('User does not exist.'))


@app.route('/user', methods=['POST'])
@auth.login_required
def create_user():
    """ Creates a User. """
    data = request.get_json()
    try:
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(encrypted_status_response('New User Created.'))
    except IntegrityError:
        return jsonify(encrypted_status_response(
            'A user already exists with same username or email.'
            )
        )


@app.route('/user/<username>', methods=['PUT'])
@auth.login_required
def update_user(username):
    """ Updates User data. """
    data = request.get_json()
    user = User.query.filter_by(username=username).first()
    if user:
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.user_name = data['username']
        user.email = data['email']
        user.password = data['password']
        db.session.commit()
        return jsonify(encrypted_status_response('Updated User Data.'))
    return jsonify(encrypted_status_response('User not Found.'))


@app.route('/user/<username>', methods=['DELETE'])
@auth.login_required
def delete_user(username):
    """ Deletes the User. """
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(encrypted_status_response('User Deleted.'))
    return jsonify(encrypted_status_response('User not Found.'))


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
