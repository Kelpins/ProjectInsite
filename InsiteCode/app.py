from flask import Flask, render_template, request, redirect, url_for, flash
import io
import requests
from PIL import Image as fja
import sys
import json
import forms
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# Models requires app and db, import after those are defined to avoid circular import
from models import User, Page, PageComponent

# Currently unnecessary but may be useful for future image resizing
def getsizes(url):
    image_content = requests.get(url).content
    image_stream = io.BytesIO(image_content)
    img = fja.open(image_stream)
    size = img.size
    screenWidth = 1680
    width = size[0]
    height = ((screenWidth/4) * size[1]) / width
    results = [screenWidth/4, height]
    return results

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Page': Page, 'PageComponent': PageComponent}

filepath = "static/burnie6.json"
file = open(filepath)
data = json.load(file)
login.login_view = 'login'

data["index"].update(data["base"])
data["about"].update(data["base"])
data["privacy"].update(data["base"])
data["empty"].update(data["base"])
for page in data["new"].keys():
    data["new"][page].update(data["base"])

#Routers

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # only accepts relative URLs, not absolute ones (i.e. no outside websites)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('wtform')
        return redirect(next_page)    
    return render_template('login.html.j2', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=["GET", "POST"])
@login_required
def wtform():
    # Use this if we need to reset the field data
    # filepathWTF = "static/burnie6.json"
    # fileWTF = open(filepathWTF)
    # dataWTF = json.load(fileWTF)
    formWTF = forms.BigForm(data=data)
    if formWTF.validate_on_submit():
        # Add form data to database
        for field in formWTF.index:
            # print(field.short_name)
            data["index"][field.short_name] = field.data
        for field in formWTF.about:
            # print(field.short_name)
            # There's no direct connections to the cards, because of topCards and bottomCards
            data["about"][field.short_name] = field.data
        for field in formWTF.privacy:
            # print(field.short_name)
            data["privacy"][field.short_name] = field.data
        return redirect('/index')
    else:
        print(formWTF.errors)
    return render_template('wtform.html.j2', form=formWTF)

# Generalize this to also work for the new pages
@app.route('/addParagraph')
def addParagraph():
    data["index"]["paragraphs"].append({"text" : ""})
    return redirect(url_for('wtform'))

@app.route('/addPage')
def addPage():
    # Keep a counter and generate page names as "page1", "page2", etc.
    newPageCount = len(data["new"].keys()) + 1
    data["base"]["pages"]["page"+str(newPageCount)] = {"Name" : "page"+str(newPageCount), "Link" : "page"+str(newPageCount)}
    # The IDs in baseVars["pages"] and the keys of newVars should always match exactly (except for home/about)
    # Each new page has the values from emptyVars as default
    data["new"]["page"+str(newPageCount)] = {k:v for k, v in data["empty"].items()}
    return redirect(url_for('wtform'))
    
@app.route('/privacy-policy')
@login_required
def privacy():
    return render_template('privacy-policy.html.j2', **data["privacy"])

# @app.route('/index')
# def indexRoute():
#     return render_template('index.html.j2', **indexVars)

@app.route('/<route>')
@login_required
def router(route):
    pages = data["base"]["pages"].keys()
    # routes is a list of all possible pages except privacy-policy, form, and login
    routes = {}
    # newRoutes has new page links as keys and page IDs as values
    # newRoutes = {}
    # print("All new pages: " + str(newVars.keys()))
    for page in pages:
        link = data["base"]["pages"][page]["Link"]
        routes[link] = page
        # Previously used page["Name"]
        # if page in newVars.keys():
        #     newRoutes[link] = page
            # print("New routes found: " + str(newRoutes))

    if route in routes.keys():
        pageID = routes[route]
        if pageID == "index":
            return render_template('index.html.j2', **data["index"])
        elif pageID == "about":
            return render_template('about.html.j2', **data["about"])
        # Pair a specific set of newVars with each page route
        # elif route in newRoutes.keys():
        else:
            # print("New page: " + pageName)
            return render_template('emptyTextPage.html.j2', **data["new"][pageID])
        # else:
        #     return render_template('emptyTextPage.html.j2', **emptyVars)
    else:
        return "ILLEGAL PAGE!!!"