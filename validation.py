import re

PAYLOAD_FIELDS = {'name', 'number'}
ACCEPTABLE_QUERY_ARGUMENTS = {'page','limit','cursor','search','number'}

class ValidationError(Exception):
    pass

def validate_data(data: dict | None, request_method: str) -> dict:

    if data is None or len(data) == 0:
        raise ValidationError("Invalid JSON payload.")
    
    data_fields = set(data.keys())

    if request_method == 'POST':

        if len(data_fields) != len(PAYLOAD_FIELDS):
            raise ValidationError("Invalid number of fields.")

        if not PAYLOAD_FIELDS.issubset(data_fields):
            raise ValidationError("Missing required fields.")

        if not name_is_valid(data['name']):
            raise ValidationError(invalid_format_msg('name','[A-Za-z] and whitespace','1-100'))

        if not number_is_valid(data['number']):
            raise ValidationError(invalid_format_msg('number','[0-9]','7-15'))

    elif request_method == 'PUT':

        if len(data_fields) > len(PAYLOAD_FIELDS):
            raise ValidationError("Invalid number of fields.")

        if not data_fields.issubset(PAYLOAD_FIELDS):
            raise ValidationError("Missing required fields.")
        
        if 'name' in data:
            if not name_is_valid(data['name']):
                raise ValidationError(invalid_format_msg('name','[A-Za-z] and whitespace','1-100'))
        if 'number' in data:
            if not number_is_valid(data['number']):
                raise ValidationError(invalid_format_msg('number','[0-9]','7-15'))

    return data

def name_is_valid(name):

    if name is None:
        return False

    if len(name) < 1 or len(name) > 100:
        return False

    return bool(re.match(r'^[A-Za-z\s]+$', name.strip()))

def number_is_valid(number):

    if number is None:
        return False

    if len(number) < 7 or len(number) > 15:
        return False

    return bool(re.match(r'^\d+$', number))

def invalid_format_msg(field:str,characters_group:str,length_range:str) -> str:

    return f'Field: {field}. Error: Invalid format. Acceptable characters: {characters_group}. Acceptable length: {length_range}.'

def validate_pagination_argument(arg: str|None) ->int|None:

    if arg is None:
        return None
    
    if not bool(re.match(r'^\d+$', arg)):
            raise ValidationError('Pagination arguments should be positive integers')
    
    return int(arg)

def validate_query_keys(arguments:dict) -> None:

    args = arguments.copy()
    if not set(args).issubset(ACCEPTABLE_QUERY_ARGUMENTS):
        raise ValidationError("Request includes one or more unknown arguments.")