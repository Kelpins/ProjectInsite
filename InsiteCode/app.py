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
newVars = {}

filepath = "static/template4.json"

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
# print(data["newVars"].keys())
for page in data["newVars"].keys():
    newVars[page] = {}
    for i in data["newVars"][page]:
        key = i
        value = data["newVars"][page][i]
        if str(value).split("*****")[0] == "var":
            newVars[page][key] = data[str(value).split("*****")[1]]
        elif str(value).split("*****")[0] == "func":
            newVars[page][key] = eval(str(value).split("*****")[1])
        else:
            # print("Page: " + page)
            # print("Key: " + key)
            # print("Value: " + value)
            newVars[page][key] = value
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
for page in newVars.keys():
    newVars[page].update(baseVars)

#Routers
@app.route('/')
def form():
    formVars = {
        "baseVars" : baseVars,
        "indexVars" : indexVars,
        "aboutVars" : aboutVars,
        "privacyVars" : privacyVars,
        "emptyVars" : emptyVars,
        "newVars" : newVars
    }
    return render_template('form.html.j2', **formVars)

@app.route('/generate', methods=["POST"])
def generateWebsite():
    website_data = request.form
    for item in website_data:
        # print(item)
        key = item
        value = website_data[item]
        prefix = key.split("-")[0]
        id = prefix + "-"
        name = key.split("-")[1]

        if id[0] == "b":
            if id[1] == "-":
                baseVars[name] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                # Reformat baseVars["pages"] as a simple dictionary: keys are names, values are links    
                baseVars["pages"][int(num)][str(name)] = value
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
        # Changed this because p applies to new pages
        elif id[0] == "r":
            if id[1] == "-":
                privacyVars[key[1:]] = value
            else:
                return "PRIVACY BORKED!!! -- 003"
        # Change this stuff
        elif prefix in newVars.keys():
            # print("New page prefix: " + prefix)
            if id[len(id)-1] == "-":
                newVars[prefix][name] = value
            elif id[len(id)-1] == "p":
                num = id.split("-")[0].split("p")[1]
                newVars[prefix]["paragraphs"][int(num)][name] = value
            else:
                return "New page BORKED!!! -- 004"
        else:
            print("Empty prefix " + prefix)
            if id[1] == "-":
                emptyVars[name] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                emptyVars["paragraphs"][int(num)][name] = value
            else:
                return "EMPTY BORKED!!! -- 004"
    return redirect('/index')

# Generalize this to also work for the new pages
@app.route('/addParagraph')
def addParagraph():
    indexVars["paragraphs"].append({"text" : ""})
    return redirect('/')

# newPageCount = 0

@app.route('/addPage')
def addPage():
    # Reformat baseVars["pages"] as a simple dictionary: keys are names, values are links
    # Keep a counter and generate page names as "page1", "page2", etc.
    newPageCount = len(newVars.keys()) + 1
    baseVars["pages"].append({"Name" : "page"+str(newPageCount), "Link" : ""})
    # baseVars["newPages"]["page"+str(newPageCount)] = {"Link": "", "Type": "text"}
    newVars["page"+str(newPageCount)] = {}
    return redirect('/')
    
@app.route('/privacy-policy')
def privacy():
    return render_template('privacy-policy.html.j2', **privacyVars)

@app.route('/<route>')
def router(route):
    # Reformat baseVars["pages"] as a simple dictionary: keys are names, values are links
    pages = baseVars["pages"]
    routes = []
    # newRoutes has new page links as keys and page names as values
    newRoutes = {}
    # print("All new pages: " + str(newVars.keys()))
    for page in pages:
        routes.append(page["Link"])
        # print("Current page: " + page["Name"])
        if page["Name"] in newVars.keys():
            newRoutes[page["Link"]] = page["Name"]
            # print("New routes found: " + str(newRoutes))

    if route in routes:
        # Can this break if you change the page route in the submission form?
        if route == "index":
            return render_template('index.html.j2', **indexVars)
        elif route == "about":
            return render_template('about.html.j2', **aboutVars)
        # Pair a specific set of newVars with each page route
        elif route in newRoutes.keys():
            pageName = newRoutes[route]
            # print("New page: " + pageName)
            return render_template('emptyTextPage.html.j2', **newVars[pageName])
        else:
            return render_template('emptyTextPage.html.j2', **emptyVars)
    else:
        return "ILLEGAL PAGE!!!"