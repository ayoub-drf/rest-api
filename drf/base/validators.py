from rest_framework.exceptions import ValidationError

def positive_number(value):
    if value <= 0:
        raise ValidationError("Value must be a positive number.")
    
    return value