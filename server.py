from flask import Flask, request, jsonify

app = Flask(__name__)

contacts = [
    {"id": 1, "name": "john", "number": "6985699842"},
    {"id": 2, "name": "adam", "number": "6985239842"},
    {"id": 3, "name": "peter", "number": "6985645842"},
]

# GET    - /contacts - list contacts
# GET    - /contacts/<id> - list specific contact
# POST   - /contacts - add contact
# PUT    - /contacts/<id> - edit contact
# DELETE - /contacts/<id> - delete contact


def createResponse(
    data: list | dict | None = None,
    success: bool = True,
    errMsg: str | None = None,
    errCode: int | None = None,
):
    
    #This function returns a JSON response based on given arguments.
    #Usage examples:
    #Success: createResponse(data = data)
    #Failure: createResponse(success=False,errMsg='<short status message>',errCode = '<http status code>')
    

    if success:
        response = {"success": True, "data": data, "error": None}
    else:
        response = {
            "success": False,
            "data": None,
            "error": {"message": errMsg, "code": errCode},
        }
    
    return jsonify(response)


@app.errorhandler(404)
def resource_not_found(e):
    return createResponse(success=False,errMsg='SourceNotFound',errCode = 404),405

@app.errorhandler(405)
def resource_not_found(e):
    return createResponse(success=False,errMsg='InvalidRequest',errCode = 405),405

@app.errorhandler(400)
def resource_not_found(e):
    return createResponse(success=False,errMsg='BadRequest',errCode = 400),400

@app.errorhandler(500)
def resource_not_found(e):
    return createResponse(success=False,errMsg='InvalidRequest',errCode = 500),500

@app.route("/")
def homepage():
    return "<h1>Hello there!</h1>"


@app.get("/contacts")
def list_contacts():
    return (createResponse(data=contacts), 200)


@app.get("/contacts/<int:id>")
def list_contact(id):

    for contact in contacts:
        if contact["id"] == id:
            return (createResponse(data=contact), 200)

    return (
        createResponse(success=False, errMsg="SourceNotFound", errCode=404),
        404,
    )


@app.post("/contacts")
def add_contact():
    payload = request.get_json(silent=True)

    if not payload:
        return (
            createResponse(success=False, errMsg="InvalidPayload", errCode=400),
            400,
        )

    contactName = payload.get("name")
    contactNumber = payload.get("number")

    if contactName and contactNumber:
        newContact = {
            "id": max(int(c["id"]) for c in contacts) + 1 if contacts else 1,
            "name": contactName,
            "number": contactNumber,
        }

        contacts.append(newContact)

        return createResponse(data=newContact), 201

    return (
        createResponse(success=False, errMsg="InvalidPayload", errCode=400),
        400,
    )


@app.put("/contacts/<int:id>")
def edit_contact(id):

    payload = request.get_json(silent=True)

    if not payload:
        return (
            createResponse(success=False, errMsg="InvalidPayload", errCode=400),
            400,
        )

    contactName = payload.get("name")
    contactNumber = payload.get("number")

    for contact in contacts:
        if contact["id"] == id:
            contact["name"] = contactName if contactName else contact["name"]
            contact["number"] = contactNumber if contactNumber else contact["number"]

            return (createResponse(data=contact), 200)

    return (
        createResponse(success=False, errMsg="SourceNotFound", errCode=404),
        404,
    )


@app.delete("/contacts/<int:id>")
def delete_contact(id):

    for contact in contacts:
        if contact["id"] == id:
            contacts.remove(contact)
            return ("", 204)

    return (
        createResponse(success=False, errMsg="SourceNotFound", errCode=404),
        404,
    )


app.run(debug=True)
