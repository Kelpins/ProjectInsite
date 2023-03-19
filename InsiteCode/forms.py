from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, FormField, FieldList, validators


class IndexForm(FlaskForm):
    site_name = StringField('Site Name', [validators.Length(max=40)])
    instagram = StringField('Instagram Link')
    twitter = StringField('Twitter Link')
    email = StringField('Email')
    left_col = StringField('Left Column Header')
    # Paragraphs: tie min number to the data from content JSONs
    paragraphs = FieldList(StringField("Text"), min_entries=9)

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
    text_header = StringField("Text Header")
    text_subheader = StringField("Text Subheader")
    paragraphs = FieldList(StringField('Text'), min_entries=9)

class BigForm(FlaskForm):
    # This will contain everything our original form page did
    index = FormField(IndexForm)
    about = FormField(AboutForm)
    privacy = FormField(PrivacyForm)
    new = FormField(NewPageForm)
    submit = SubmitField('Generate Website')