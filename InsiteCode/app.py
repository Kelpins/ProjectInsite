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

"""
baseVars = {
    
    "navBtnClass" : "btn btn-primary",
    "pages" : [("Home", "/index"), ("About", "/about")],
    "navbar_right" : "so much more than a body coach",
    "copyright" : "©Copyright 2022. All rights reserved."
    
}

indexParagraphs2 = [

    {"text" : "In this guest blog post, Dr Louise Newson explains the essentials of perimenopause and menopause and talks about how exercise and good nutrition can help with the symptoms."},
    {"text" : "For decades, the menopause has been a taboo and there has been a huge amount of misinformation and misconceptions about treatment options, especially hormone replacement therapy (HRT). This has resulted in women's health being far worse than it could be otherwise. If more women were given the right advice and treatment based on the available evidence, women's health would improve and health costs to the NHS and other healthcare systems globally would also dramatically reduce."},
    {"text" : "What is the menopause?", "style" : ["font-weight", "bold"]},
    {"text" : "The menopause is when the ovaries stop producing eggs and levels of hormones oestrogen, progesterone and testosterone fall."},
    {"text" : "The definition of menopause is when a woman hasn't had a period for 12 months, and the average age of the menopause in the UK is 51. However, it's really important to state that it doesn't just happen in mid-life: menopause before 45 is known as an early menopause, while menopause before the age of 40 is known as premature ovarian insufficiency (POI)."},
    {"text" : "POI is a lot more common than most people think: it affects about 1 in 100 women under the age of 40, and 1 in 1,000 women under 30. Even girls in their teens can be perimenopausal or menopausal."},
    {"text" : "For most women with POI, the underlying cause is unknown, but it can be triggered by events such as having your ovaries removed, a hysterectomy, radiotherapy to the pelvic area as a treatment for cancer or if you have received certain types of chemotherapy drugs that treat cancer. In addition, eating disorders can lead to early menopause in some women."},
    {"text" : "What is the perimenopause?", "style" : ["font-weight", "bold"]},
    {"text" : "The perimenopause is the time directly before the menopause, when you still have periods, but the fluctuating and low hormone levels - especially oestrogen - can trigger a whole host of symptoms."},
    {"text" : "There is no blood test for the perimenopause or menopause - they can often be diagnosed by completing a Menopause Symptom Questionnaire."}
]

indexVars = {
    "isDict" : "True"


    "smBtnClass" : "btn btn-primary",
    "head_img" : "static/HomeHeader.png",
    "head_height" : "400px",
    "head_color" : "rgba(0, 20, 74, 0.5)",
    "head_img_pos" : "61% 21%",
    "instagram" : "https://www.instagram.com/burnie/",
    "twitter" : "https://www.twitter.com/burnie",
    "email" : "mailto:kellan@edgy.org",
    "site_name" : "Joe's Blog",
    "right_col_img" : "https://images.ctfassets.net/izjiv8mj8dix/2LToZKzzlJ1HwibI8WVzxe/daa1a9040991fa4b17d76f036b234701/desilesphotography-105.jpg?w=2560&h=1707&q=80&fm=webp",
    "img_alt" : "existing joe",
    "img_width" : getsizes("https://images.ctfassets.net/izjiv8mj8dix/2LToZKzzlJ1HwibI8WVzxe/daa1a9040991fa4b17d76f036b234701/desilesphotography-105.jpg?w=2560&h=1707&q=80&fm=webp")[0],
    "img_height" : getsizes("https://images.ctfassets.net/izjiv8mj8dix/2LToZKzzlJ1HwibI8WVzxe/daa1a9040991fa4b17d76f036b234701/desilesphotography-105.jpg?w=2560&h=1707&q=80&fm=webp")[1],
    "left_col" : "Perimenopause and Menopause Essentials",
    "paragraphs" : indexParagraphs2
}

topCards = [


    # block 1
    {
        "img" : "static/LeaningBurnie.jpg",
        "img_name" : "leaning burnie",
        "heading" : "Smooth",
        "text" : "Writer. Director. Father. One hundred percent lifetime field goal kicker. Entrepreneur. Actor. Cheeseburger. Large Coke. To Go."
    },
    # block 2
    {
        "img" : "static/CoolBurnie.jpg",
        "img_name" : "cool burnie",
        "heading" : "Self-dressing",
        "text" : "Zippers. Buttons. Nothing curbs his pure passion for putting on clothes to protect himself from the elements."
    },
    # block 3
    {
        "img" : "static/YoungBurnie.jpg",
        "img_name" : "young burnie top",
        "heading" : "1400 on the SAT",
        "text" : "Suck it, Bobby. You had to go to Tech."
    }
]

bottomCards = [


    # block 4
    {
        "img" : "static/GunKids.jpg",
        "img_name" : "gun kids",
        "heading" : "Prepared for the future with weaponized youth",
        "text" : "Radicalizing children since 2002. Volume discounts."
    },
    # block 5
    {
        "img" : "static/Wife.jpg",
        "img_name" : "wife",
        "heading" : "Wife. Now with butt",
        "text" : "She doesn't know this was posted. Exhibit A, Divorce Proceedings."
    },
    # block 6
    {
        "img" : "static/YoungBurnie2.jpg",
        "img_name" : "young burnie bottom",
        "heading" : "Three pieces of wide collared manhood",
        "text" : "While you were reading this, he stole your girl. No take backs, champ."
    }
]

aboutVars = {
    "isDict" : "True"


    "head_img" : "static/AboutHeader.png",
    "head_height" : "700px",
    "head_color" : "rgba(21, 151, 238, 0.5)",
    "head_img_pos" : "57% 46%",
    "head_blurb" : "You ever have a dream so boring, that in it you were reading the About page on a middle-aged influencer's website?",
    "body_title" : "Our Commitment to Excellents",
    "body_subtitle" : "Elusive. Gentle. Sublime. Sanguine. Words.",
    "topCards" : topCards,
    "bottomCards" : bottomCards
}

privacyVars = {
    "isDict" : "True"


    "head_img" : "static/PrivacyHeader.png",
    "head_height" : "600px",
    "head_color" : "rgba(68, 68, 68, 0.5)",
    "head_img_pos" : "51% 35%",
    "head_blurb" : "Listen. You just mind your own beeswax and I'll mind mine.", 
    "body_text" : "Void in the EU. Don't even look at this or I'm calling the gendarmes, Pierre."
}
"""

baseVars = {}
indexVars = {}
aboutVars = {}
privacyVars = {}

filepath = "static/template1.json"

file = open(filepath)
data = json.load(file)

for i in data["baseVars"]:
    key = i
    value = data["baseVars"][i]
    if str(value)[0:4] == "var-":
        baseVars[key] = data[str(value)[4:]]
    else:
        baseVars[key] = value
for i in data["indexVars"]:
    key = i
    value = data["indexVars"][i]
    if str(value)[0:4] == "var-":
        indexVars[key] = data[str(value)[4:]]
    else:
        indexVars[key] = value
for i in data["aboutVars"]:
    key = i
    value = data["aboutVars"][i]
    if str(value)[0:4] == "var-":
        aboutVars[key] = data[str(value)[4:]]
    else:
        aboutVars[key] = value
for i in data["privacyVars"]:
    key = i
    value = data["privacyVars"][i]
    if str(value)[0:4] == "var-":
        privacyVars[key] = data[str(value)[4:]]
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
            else:
                return "SOMETHING BORKED!!! -- 000"
        elif id[0] == "i":
            if id[1] == "-":
                indexVars[name] = value
            elif key[1] == "p":
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
        elif key[0] == "p":
            if key[1] == "-":
                privacyVars[key[1:]] = value
            else:
                return "SOMETHING BORKED!!! -- 003"
    return redirect('/index')

@app.route('/addParagraph')
def addParagraph():
    indexVars["paragraphs"].append({"text" : ""})
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

# @app.route('/register')
# def register():
#     return render_template('register.html.j2')
#
# @app.route('/create')
# def namePage():
#     return render_template('name.html.j2')
#
# @app.route('/upload', methods=["GET", "POST"])
# def uploadPage():
#     name = request.values.get("websiteName")
#     type = request.values.get("webType")
#     webData.append(name)
#     webData.append(type)
#     return render_template('upload.html.j2')

#@app.route('/templates', methods=["GET", "POST"])
#def templatePage():
#    files = request.values.get("files")
#    webData.append(files)
#    return render_template('templates.html.j2')

# @app.route('/editwebsite', methods=["GET", "POST"])
# def create():
#     return render_template('editwebsite.html.j2', name=webData[0], webType=webData[1], files=webData[2])
#
# @app.route('/editwebsite', methods=["GET", "POST"])
# def generateWebsite():
#     name = request.values.get("websiteName")
#     return render_template('editwebsite.html.j2', name=name)

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
