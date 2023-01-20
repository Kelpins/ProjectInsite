from flask import Flask, render_template, request, redirect
import io
import requests
from PIL import Image as fja
import sys
import json

app = Flask(__name__)


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

baseVars = {}
indexVars = {}
aboutVars = {}
privacyVars = {}

filepath = "static/template2.json"

file = open(filepath)
data = json.load(file)

for i in data["baseVars"]:
    key = i
    value = data["baseVars"][i]
    if str(value).split("*****")[0] == "var":
        baseVars[key] = data[str(value).split("*****")[1]]
    else:
        baseVars[key] = value
for i in data["indexVars"]:
    key = i
    value = data["indexVars"][i]
    if str(value).split("*****")[0] == "var":
        indexVars[key] = data[str(value).split("*****")[1]]
    elif str(value).split("*****")[0] == "func":
        indexVars[key] = eval(str(value).split("*****")[1])
    else:
        indexVars[key] = value
for i in data["aboutVars"]:
    key = i
    value = data["aboutVars"][i]
    if str(value).split("*****")[0] == "var":
        aboutVars[key] = data[str(value).split("*****")[1]]
    else:
        aboutVars[key] = value
for i in data["privacyVars"]:
    key = i
    value = data["privacyVars"][i]
    if str(value).split("*****")[0] == "var":
        privacyVars[key] = data[str(value).split("*****")[1]]
    else:
        privacyVars[key] = value

print(baseVars)
print(indexVars)
print(aboutVars)
print(indexVars)

indexVars.update(baseVars)
aboutVars.update(baseVars)
privacyVars.update(baseVars)

#Routers
@app.route('/')
def form():
    formVars = {
        "baseVars" : baseVars,
        "indexVars" : indexVars,
        "aboutVars" : aboutVars,
        "privacyVars" : privacyVars,
    }
    return render_template('form.html.j2', **formVars)

@app.route('/generate', methods=["POST"])
def generateWebsite():
    website_data = request.form
    for item in website_data:
        key = item
        value = website_data[item]
        id = key.split("-")[0] + "-"
        name = key.split("-")[1]

        if id[0] == "b":
            if id[1] == "-":
                baseVars[name] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                print(baseVars["pages"])
                baseVars["pages"][int(num)][str(name)] = value
                print(baseVars)
            else:
                return "SOMETHING BORKED!!! -- 000"
        elif id[0] == "i":
            if id[1] == "-":
                indexVars[name] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                indexVars["paragraphs"][int(num)][name] = value
            else:
                return "SOMETHING BORKED!!! -- 001"
        elif id[0] == "a":
            if id[1] == "-":
                aboutVars[name] = value
            elif id[1] == "t":
                num = id.split("-")[0].split("t")[1]
                aboutVars["topCards"][int(num)][name] = value
            elif id[1] == "b":
                num = id.split("-")[0].split("b")[1]
                aboutVars["bottomCards"][int(num)][name] = value
            else:
                return "SOMETHING BORKED!!! -- 002"
        elif id[0] == "p":
            if id[1] == "-":
                privacyVars[key[1:]] = value
            else:
                return "SOMETHING BORKED!!! -- 003"
    return redirect('/index')

@app.route('/addParagraph')
def addParagraph():
    indexVars["paragraphs"].append({"text" : ""})
    return redirect('/')

@app.route('/addPage')
def addPage():
    baseVars["pages"].append({"Name" : "", "Link" : ""})
    return redirect('/')

@app.route('/index')
def index():
    return render_template('index.html.j2', **indexVars)

@app.route('/about')
def about():
    return render_template('about.html.j2', **aboutVars)

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy-policy.html.j2', **privacyVars)

"""
@app.route('/test', methods=["POST"])
def test():
    #Receives the variables for server side validation and in case they are to be used later(for emailing and such)
    username = request.values.get("uname")
    pwd = request.values.get("pwd")
    fname = request.values.get("fname")
    lname = request.values.get("lname")
    name = fname + " " + lname
    dob = request.values.get("dob")
    email = request.values.get("email")
    phonenum = request.values.get("phnnum")
    #reformatting phone number
    phonenum = "(" + phonenum[0:3] + ") " + phonenum[3:6] + "-" + phonenum[6:10]
    termsandconditions = request.values.get("terms")
    emails = request.values.get("emails")

    #Server side validation - if they left one form empty or turned off the terms and conditions checkbox but somehow got to this point in the code it sends them to the hacker page
    if username == "" or pwd == "" or fname == "" or lname == "" or dob == "" or email == "" or phonenum == "" or termsandconditions != "on":
        return render_template('hacker.html.j2')

    #Routes to IQ test
    terms = generateSeries(5)

    return render_template('test.html.j2', terms=terms, username=username, pwd=pwd, name=name, dob=dob, email=email, phonenum=phonenum, termsandconditions=termsandconditions, emails=emails)
"""
