from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, validators

class BigForm(FlaskForm):
    index = FormField(IndexForm)
    about = FormField(AboutForm)

class IndexForm(FlaskForm):
    site_name = StringField('Site Name', [validators.Length(max=40)])
    instagram = StringField('Instagram Link')
    twitter = StringField('Twitter Link')
    email = StringField('Email')
    left_col = StringField('Left Column Header')
    paragraphs = FieldList(StringField(), min=0)
    # Fields for paragraphs: tie number to the data from content JSONs


class AboutForm(FlaskForm):
    head_blurb = StringField('Head Blurb')
    

# class PrivacyForm(FlaskForm):
    