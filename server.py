from flask import Flask

app = Flask(__name__)

contactsList = [
    {'id':'1','name':'john','number':'6985699842'},
]


@app.route('/')
def homepage():
    return '<h1>Hello there!</h1>'

@app.get('/contacts')
def list_contacts():
    return contactsList

app.run(debug=True)

