from flask_marshmallow import Schema
from marshmallow.fields import Str, Email
from marshmallow import validate 

length = validate.Length(min=1)

class AuthApi(Schema):
    class Meta:
        fields = ["email_id", "password"]
    email_id = Email(validate=length, required=True)
    password = Str(validate=length)


