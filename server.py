from flask import Flask,request,jsonify
import json

app = Flask(__name__)

contacts = [
    {'id':'1','name':'john','number':'6985699842'},
    {'id':'2','name':'adam','number':'6985239842'},
    {'id':'3','name':'peter','number':'6985645842'},
]


@app.route('/')
def homepage():
    return '<h1>Hello there!</h1>'

@app.get('/contacts')
def list_contacts():
    return json.dumps(contacts)

@app.get('/contacts/<id>')
def list_contact(id):
    for contact in contacts:
        if contact['id'] == id:
            return jsonify(contact)
        
    return ('No matching record for requested id',404)

@app.post('/contacts')
def add_contact():
    contactId = request.json['id']
    contactName = request.json['name']
    contactNumber = request.json['number']

    if contactId and contactName and contactNumber:
        newContact = {
            'id':contactId,
            'name':contactName,
            'number':contactNumber
        }

        contacts.append(newContact)


        return newContact
    
    return ('Something went wrong while adding your contact',400)

@app.put('/contacts/<id>')
def edit_contact(id):
    contactName = request.json['name']
    contactNumber = request.json['number']

    for contact in contacts:
        if contact['id'] == id:
            contact['name'] = contactName if contactName else contact['name']
            contact['number'] = contactNumber if contactNumber else contact['number']
            return jsonify(contact)
        
    return ('Could not find requested id',400)

@app.delete('/contacts/<id>')
def delete_contact(id):

    for contact in contacts:
        if contact['id'] == id:
            contacts.remove(contact)
            return 'Removed successfully'
        
    return ('Could not find requested id',400)

app.run(debug=True)

