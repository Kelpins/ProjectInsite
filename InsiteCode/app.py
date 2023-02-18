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
# Make emptyVars a list, with each entry being a specific page's vars
emptyVars = {}

filepath = "static/template3.json"

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
for i in data["emptyVars"]:
    key = i
    value = data["emptyVars"][i]
    if str(value).split("*****")[0] == "var":
        emptyVars[key] = data[str(value).split("*****")[1]]
    elif str(value).split("*****")[0] == "func":
        emptyVars[key] = eval(str(value).split("*****")[1])
    else:
        emptyVars[key] = value
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

indexVars.update(baseVars)
aboutVars.update(baseVars)
privacyVars.update(baseVars)
emptyVars.update(baseVars)

#Routers
@app.route('/')
def form():
    formVars = {
        "baseVars" : baseVars,
        "indexVars" : indexVars,
        "aboutVars" : aboutVars,
        "privacyVars" : privacyVars,
        "emptyVars" : emptyVars,
    }
    return render_template('form.html.j2', **formVars)

@app.route('/generate', methods=["POST"])
def generateWebsite():
    website_data = request.form
    for item in website_data:
        # print(item)
        key = item
        value = website_data[item]
        id = key.split("-")[0] + "-"
        name = key.split("-")[1]

        if id[0] == "b":
            if id[1] == "-":
                baseVars[name] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                # print(baseVars["pages"])
                baseVars["pages"][int(num)][str(name)] = value
                # print(baseVars)
            else:
                return "BASE BORKED!!!"
        elif id[0] == "i":
            if id[1] == "-":
                indexVars[name] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                indexVars["paragraphs"][int(num)][name] = value
            else:
                return "INDEX BORKED!!!"
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
                return "ABOUT BORKED!!!"
        elif id[0] == "p":
            if id[1] == "-":
                privacyVars[key[1:]] = value
            else:
                return "PRIVACY BORKED!!! -- 003"
        elif id[0] == "e":
            if id[1] == "-":
                emptyVars[name] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                emptyVars["paragraphs"][int(num)][name] = value
            else:
                return "EMPTY BORKED!!! -- 004"
    return redirect('/index')

@app.route('/addParagraph')
def addParagraph():
    indexVars["paragraphs"].append({"text" : ""})
    return redirect('/')

@app.route('/addPage')
def addPage():
    baseVars["pages"].append({"Name" : "", "Link" : ""})
    return redirect('/')
    

@app.route('/<route>')
def router(route):
    # print(baseVars)
    pages = baseVars["pages"]
    routes = []
    for page in pages:
        routes.append(page["Link"])
    # print(route + "HIASHDFLKIAHSDLJKFHAKSJHFGAKJSDFG")
    # print(routes)
    if route in routes:
        if route == "index":
            return render_template('index.html.j2', **indexVars)
        elif route == "about":
            return render_template('about.html.j2', **aboutVars)
        elif route == "privacy-policy":
            return render_template('privacy-policy.html.j2', **privacyVars)
        # Make this a variable for whatever the new page is
        else:
            return render_template('emptyPageTemplate.html.j2', **emptyVars)
    else:
        return "ILLEGAL PAGE!!!"