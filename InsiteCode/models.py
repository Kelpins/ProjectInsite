from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# We have a user table (for logins and such), pages table, pagecomponents table
# Currently each user can have one website, add another website table if that changes

@login.user_loader
def load_user(id):
    # id comes as a string in flask-login
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pages = db.relationship('Page', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(64))
    title = db.Column(db.String(128))
    components = db.relationship('PageComponent', backref='page', lazy='dynamic')

    def __repr__(self):
        return '<Page: {} Template: {}>'.format(self.title, self.type)

class PageComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    type = db.Column(db.String(64))
    key = db.Column(db.String(128))
    value = db.Column(db.String(256))

    def __repr__(self):
        return '<Page: {} Component: {} Content: {}>'.format(self.page_id, self.key, self.value)


