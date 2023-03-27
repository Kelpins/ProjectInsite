from flask import Flask, render_template, request, redirect, url_for
import io
import requests
from PIL import Image as fja

app = Flask(__name__)

baseVars = {
    "navBtnClass" : "btn btn-primary",
    "pages" : [{"Name": "home", "Link": "/"}, {"Name": "about", "Link": "about"}],
    "navbar_right" : "so much more than a body coach",
    "copyright" : "©Copyright 2022. All rights reserved."
}

topCards = [
    # block 1
    {
        "img" : "static/burniekid.jpeg",
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
    "body_title" : "Burnie",
    "body_subtitle" : "Burnie Burns",
    "body_desc" : "Writer, Producer and Director. Dad x3",
    "img" : "static/burnieHeadshot.jpg",
    "img_name" : "leaning burnie",
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

emptyVars = {
    "page_title" : "New Page",
    "page_header" : "Page Header",
    "page_subheader" : "Page Subheader",
    "body_title" : "Burnie",
    "body_subtitle" : "Elusive. Gentle. Sublime. Sanguine. Words.",
    "topCards" : topCards,
    "bottomCards" : bottomCards
}

aboutVars.update(baseVars)
privacyVars.update(baseVars)
emptyVars.update(baseVars)

@app.route('/')
def index():
    return render_template('about.html.j2', **aboutVars)

@app.route('/privacy-policy')
def privacy():
    return render_template('privacy-policy.html.j2', **privacyVars)

@app.route('/<whatever>')
def about(whatever):
    return render_template('emptyCardPage.html.j2', **emptyVars)