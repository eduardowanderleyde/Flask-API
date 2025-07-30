from marshmallow import Schema, fields, validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.user import User


class UserSchema(SQLAlchemyAutoSchema):
    """Schema for user serialization."""
    
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)


class UserRegisterSchema(Schema):
    """Schema for user registration."""
    
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    confirm_password = fields.Str(required=True)
    
    def validate_confirm_password(self, value, data, **kwargs):
        """Validate that passwords match."""
        if value != data.get('password'):
            raise ValidationError('Passwords do not match.')
        return value


class UserLoginSchema(Schema):
    """Schema for user login."""
    
    username = fields.Str(required=True)
    password = fields.Str(required=True) 