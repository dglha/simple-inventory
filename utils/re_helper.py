import re

PHONE_REGULAR_EXPRESSION = "^[0-9\-\+]{9,15}$"
EMAIL_REGULAR_EXPRESSION = "^[a-z][a-z0-9_\.]{5,32}@[a-z0-9]{2,}(\.[a-z0-9]{2,4}){1,2}"

def is_valid_phone(phone: str):
    return re.match(PHONE_REGULAR_EXPRESSION, phone)

def is_valid_email(email: str):
    return re.match(EMAIL_REGULAR_EXPRESSION, email)