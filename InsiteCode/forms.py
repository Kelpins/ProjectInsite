from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, FormField, FieldList, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # Checks if user is already in the users table
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Checks if email is already in the users table
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class IndexForm(FlaskForm):
    site_name = StringField('Site Name', [Length(max=40)])
    instagram = StringField('Instagram Link')
    twitter = StringField('Twitter Link')
    email = StringField('Email')
    left_col = StringField('Left Column Header')
    # Paragraphs: tie min number to the data from content JSONs
    paragraphs = FieldList(StringField('Text'), min_entries=9)

class CardForm(Form):
    heading = StringField('Heading')
    text = StringField('Text')

class AboutForm(FlaskForm):
    head_blurb = StringField('Head Blurb')
    body_title = StringField('Body Title')
    body_subtitle = StringField('Body Subtitle')
    # About page has 6 cards by default
    cards = FieldList(FormField(CardForm), min_entries=6)

class PrivacyForm(FlaskForm):
    head_blurb = StringField('Head Blurb')
    body_text = StringField('Body Text')

class NewPageForm(FlaskForm):
    page_title = StringField('Page Title')
    page_header = StringField('Page Header')
    page_subheader = StringField('Page Subheader')
    text_header = StringField('Text Header')
    text_subheader = StringField('Text Subheader')
    paragraphs = FieldList(StringField('Text'), min_entries=9)

class BigForm(FlaskForm):
    # This will contain everything our original form page did
    index = FormField(IndexForm)
    about = FormField(AboutForm)
    privacy = FormField(PrivacyForm)
    new = FormField(NewPageForm)
    submit = SubmitField('Generate Website')