from app import db

# We have a user table (for logins and such), pages table, pagecomponents table
# Currently each user can have one website, add another website table if that changes

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pages = db.relationship('Page', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

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


