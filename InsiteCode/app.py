from flask import Flask, render_template, request, redirect, url_for
import io
import requests
from PIL import Image as fja
import sys
import json
import forms
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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

filepath = "static/burnie4.json"

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
        # The paragraphs for new pages are not editable because they are passed by reference from emptyVars
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

# New route for form page, uses WTForms
@app.route('/', methods=["GET", "POST"])
def wtform():
    filepathWTF = "static/burnie5.json"
    fileWTF = open(filepathWTF)
    dataWTF = json.load(fileWTF)
    formWTF = forms.BigForm(data=dataWTF)
    if formWTF.validate_on_submit():
        for field in formWTF.index:
            print(field.short_name)
            if field.short_name == "paragraphs":
                for i in range(len(field.data)):
                    print(field.data[i])
                    indexVars["paragraphs"][i] = field.data[i]
                print(indexVars["paragraphs"])
            else:
                indexVars[field.short_name] = field.data
        for field in formWTF.about:
            print(field.short_name)
            aboutVars[field.short_name] = field.data
        for field in formWTF.privacy:
            print(field.short_name)
            privacyVars[field.short_name] = field.data
        return redirect('/index')
    else:
        print(formWTF.errors)
    return render_template('wtform.html.j2', form=formWTF)

# def form():
#     formVars = {
#         "baseVars" : baseVars,
#         "indexVars" : indexVars,
#         "aboutVars" : aboutVars,
#         "privacyVars" : privacyVars,
#         "emptyVars" : emptyVars,
#         "newVars" : newVars
#     }
#     return render_template('form.html.j2', **formVars)

@app.route('/generate', methods=["POST"])
def generateWebsite():
    website_data = request.form
    for item in website_data:
        key = item
        value = website_data[item]
        splitKey = key.split("-")
        prefix = splitKey[0]
        id = prefix + "-"
        # fieldName should be the last entry in splitKey, usually index 1 but sometimes index 2
        fieldName = splitKey[len(splitKey)-1]

        if id[0] == "b":
            if (len(splitKey) == 3) and (splitKey[1] in baseVars["pages"].keys()):
                # num = id.split("-")[0].split("p")[1]
                pageID = splitKey[1]
                # Previously baseVars["pages"][int(num)][str(fieldName)] = value
                # print("Key: " + key)
                # print("Value: " + value)
                # print("PageID: " + pageID)
                # print("FieldName: " + fieldName)
                baseVars["pages"][pageID][fieldName] = value
            elif id[1] == "-":
                baseVars[fieldName] = value
            else:
                return "BASE BORKED!!!"
        elif id[0] == "i":
            if id[1] == "-":
                indexVars[fieldName] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                indexVars["paragraphs"][int(num)][fieldName] = value
            else:
                return "INDEX BORKED!!!"
        elif id[0] == "a":
            if id[1] == "-":
                aboutVars[fieldName] = value
            elif id[1] == "t":
                num = id.split("-")[0].split("t")[1]
                aboutVars["topCards"][int(num)][fieldName] = value
            elif id[1] == "b":
                num = id.split("-")[0].split("b")[1]
                aboutVars["bottomCards"][int(num)][fieldName] = value
            else:
                return "ABOUT BORKED!!!"
        elif id[0] == "r":
            if id[1] == "-":
                privacyVars[key[1:]] = value
            else:
                return "PRIVACY BORKED!!! -- 003"
        # Change this stuff
        elif prefix in newVars.keys():
            # if id[len(id)-1] == "-":
            if len(splitKey) == 2:
                newVars[prefix][fieldName] = value
            # No splitting on letters my dude
            # elif id[len(id)-1] == "p":
            elif len(splitKey) == 3:
                num = splitKey[1]
                newVars[prefix]["paragraphs"][int(num)][fieldName] = value
                # print("New paragraph: " + newVars[prefix]["paragraphs"][int(num)][fieldName])
            else:
                return "New page BORKED!!! -- 004"
        else:
            print("Empty prefix " + prefix)
            if id[1] == "-":
                emptyVars[fieldName] = value
            elif id[1] == "p":
                num = id.split("-")[0].split("p")[1]
                emptyVars["paragraphs"][int(num)][fieldName] = value
            else:
                return "EMPTY BORKED!!! -- 004"
    return redirect('/index')

# Generalize this to also work for the new pages
@app.route('/addParagraph')
def addParagraph():
    indexVars["paragraphs"].append({"text" : ""})
    return redirect('/')

@app.route('/addPage')
def addPage():
    # Reformat baseVars["pages"] as a simple dictionary: keys are names, values are links
    # Keep a counter and generate page names as "page1", "page2", etc.
    newPageCount = len(newVars.keys()) + 1
    baseVars["pages"]["page"+str(newPageCount)] = {"Name" : "page"+str(newPageCount), "Link" : "page"+str(newPageCount)}
    # The IDs in baseVars["pages"] and the keys of newVars should always match exactly (except for home/about)
    # Each new page has the values from emptyVars as default
    newVars["page"+str(newPageCount)] = {k:v for k, v in emptyVars.items()}
    return redirect('/')
    
@app.route('/privacy-policy')
def privacy():
    return render_template('privacy-policy.html.j2', **privacyVars)

@app.route('/index')
def indexRoute():
    print(("Jason is scam"))
    return render_template('index.html.j2', **indexVars)

@app.route('/<route>')
def router(route):
    # Reformat baseVars["pages"] as a simple dictionary: keys are names, values are links
    pages = baseVars["pages"].keys()
    # routes is a list of all possible pages except privacy-policy
    routes = {}
    # newRoutes has new page links as keys and page IDs as values
    # newRoutes = {}
    # print("All new pages: " + str(newVars.keys()))
    for page in pages:
        link = baseVars["pages"][page]["Link"]
        routes[link] = page
        # Previously used page["Name"]
        # if page in newVars.keys():
        #     newRoutes[link] = page
            # print("New routes found: " + str(newRoutes))

    if route in routes.keys():
        pageID = routes[route]
        # Can this break if you change the page route in the submission form?
        if pageID == "index":
            return render_template('index.html.j2', **indexVars)
        elif pageID == "about":
            return render_template('about.html.j2', **aboutVars)
        # Pair a specific set of newVars with each page route
        # elif route in newRoutes.keys():
        else:
            # print("New page: " + pageName)
            return render_template('emptyTextPage.html.j2', **newVars[pageID])
        # else:
        #     return render_template('emptyTextPage.html.j2', **emptyVars)
    else:
        return "ILLEGAL PAGE!!!"