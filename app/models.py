from datetime import datetime
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from app import login
from flask import request
from werkzeug.urls import url_parse
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, RoleMixin
#flask models
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return role in self.roles

    def is_active(self):
        return True

class Movie(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    link = db.Column(db.String(280))
    description = db.Column(db.String(1120))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    poster = db.Column(db.String(280))

    def __repr__(self):
        return '<Movie {}>'.format(self.name)
#get dict to json later
    def to_dict(self):
        data = {
            'id': self.id,
            'name' : self.name,
            'link': self.link,
            'description': self.description,
            'timestamp': self.timestamp,
            'poster': self.poster
            }
        return data
#roles 
class Role(RoleMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name) 


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {} role {}>'.format(self.user_id, self.role_id) 


class MyModelView(ModelView):
    def is_accessible(self):   
        if current_user.has_role('admin'):
            return True
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
        
admin = Admin(app, index_view = MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Movie, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(UserRoles, db.session))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

