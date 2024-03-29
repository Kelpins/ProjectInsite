from flask import Flask, render_template, request

app = Flask(__name__)

baseVars = {
    "navbar_right" : "so much more than a dude playing the cowbell",
    "copyright" : "©Copyright 2022. All rights reserved."
}

indexParagraphs = [

    "In the summer of 1990, I packed everything I owned into a beat up old Nissan and set out for Austin to study Biology/PreMed at the University of Texas. Over the next thirty years, I changed majors twice, made some incredible friends, sold the car for two hundred dollars, had a wild dotcom career in telecom, raised three sons and started a small media company in a spare bedroom of my house that blossomed into something beyond my wildest dreams. It is a bit surreal that three decades later, almost to the day, I will be moving out of this city that I may always call “home” to begin a grand new adventure in a life overseas.",
    "It is difficult to leave my home country during such a tumultuous time. Ashley and I set these plans in motion over two years ago, and we could never have predicted the state of the world at the time we would embark. We believe in the strength and the promise of this nation as much as ever. We look forward to returning to a country that has made many long overdue changes to benefit all of its citizens.",
    "I want to express my deepest gratitude to everyone who supported me in my career at RT, with special thanks to Tony Goncalves who so skillfully leads the Otter family and Jordan Levin, who has RT moving in incredible new directions. Starting this company and growing it in the early years were some of the hardest but greatest moments of my life. The constant camaraderie of Gus, Geoff, and Matt always made the impossible seem achievable; I could not have asked for better companions on this journey. My wife Ashley has been the stable bedrock of my life and I am overjoyed to begin this next chapter of our family's story together.",
    "Thank you to every person who has walked through these doors as a collaborator or tuned in to one of our videos as a viewer or made the choice to become a member of our community. Your support has meant the world to me and I hope that I had even a fraction of the positive impact on your life that you have had on mine. There have been a lot of ups and a few downs over the years, and I have learned so much from all of those experiences. I am eternally grateful that I had the opportunity to do what I love every day — an opportunity that I owe entirely to all of you.",
    "Thank you.",
    "Be nice and work hard.",
    "Burnie"

]

indexVars = {
    "head_img" : "static/HomeHeader.png",
    "head_height" : "400px",
    "head_color" : "rgba(0, 20, 74, 0.5)",
    "head_img_pos" : "61% 21%",
    "instagram" : "https://www.instagram.com/burnie/",
    "twitter" : "https://www.twitter.com/burnie",
    "email" : "mailto:kellan@edgy.org",
    "site_name" : "burnie.com",
    "right_col_img" : "static/BURNIE.jpeg",
    "left_col" : "gg new map",
    "paragraphs" : indexParagraphs
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
    "head_img" : "static/PrivacyHeader.png",
    "head_height" : "600px",
    "head_color" : "rgba(68, 68, 68, 0.5)",
    "head_img_pos" : "51% 35%",
    "head_blurb" : "Listen. You just mind your own beeswax and I'll mind mine.", 
    "body_text" : "Void in the EU. Don't even look at this or I'm calling the gendarmes, Pierre."
}

indexVars.update(baseVars)
aboutVars.update(baseVars)
privacyVars.update(baseVars)

#Routers
@app.route('/')
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
