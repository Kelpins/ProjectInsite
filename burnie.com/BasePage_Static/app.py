from flask import Flask, render_template, request

app = Flask(__name__)
webData = []

#Routers
@app.route('/')
def index():
    return render_template('index.html.j2')

@app.route('/register')
def register():
    return render_template('register.html.j2')

@app.route('/create')
def namePage():
    return render_template('name.html.j2')

@app.route('/upload', methods=["GET", "POST"])
def uploadPage():
    name = request.values.get("websiteName")
    type = request.values.get("webType")
    webData.append(name)
    webData.append(type)
    return render_template('upload.html.j2')

@app.route('/templates', methods=["GET", "POST"])
def templatePage():
    files = request.values.get("files")
    webData.append(files)
    return render_template('templates.html.j2')

@app.route('/editwebsite', methods=["GET", "POST"])
def create():
    return render_template('editwebsite.html.j2', name=webData[0], webType=webData[1], files=webData[2])

@app.route('/editwebsite', methods=["GET", "POST"])
def generateWebsite():
    name = request.values.get("websiteName")
    return render_template('editwebsite.html.j2', name=name)

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