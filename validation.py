import re

JSON_ATTRIBUTES = ['name', 'number']

class ValidationError(Exception):
    pass

def validate_data(data,request_method):
    if request_method == 'POST':

        for attribute in JSON_ATTRIBUTES:
            if attribute not in data:
                raise ValidationError(f"{attribute} field is required.")

        if not name_is_valid(data['name'].strip()):
            raise ValidationError("Name is invalid. Acceptable characters [A-Za-z] and spaces. Length must be between 1 and 100 characters.")

        if not number_is_valid(data['number']):
            raise ValidationError("Number is invalid. Acceptable characters [0-9]. Length must be between 7 and 15 digits.")

    elif request_method == 'PUT':

        args_found = [key for key in data.keys() if key in JSON_ATTRIBUTES]
        if not args_found:
            raise ValidationError("Required fields are missing.")

        if not name_is_valid(data['name'].strip()):
            raise ValidationError("Invalid name format.")

        if not number_is_valid(data['number']):
            raise ValidationError("Invalid number format.")
        
    return data

def name_is_valid(name):

    if len(name) < 1 or len(name) > 100:
        return False

    return bool(re.match(r'^[A-Za-z\s]+$', name))

def number_is_valid(number):

    if len(number) < 7 or len(number) > 15:
        return False

    return bool(re.match(r'^\d+$', number))