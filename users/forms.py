import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, ValidationError, Length, EqualTo


def character_check(form, field):
    excluded_chars = "* ? ! ' ^ + % & / ( ) = } ] [ { $ # @ < >"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


def reformat_phone(form, field):
    if len(field.data) == 11:
        if field.data.isnumeric():
            form.phone.data = '{}-{}-{}'.format(field.data[0:4], field.data[4:7], field.data[7:11])
        else:
            raise ValidationError(
                f"Phone Number should be numbers only")
    else:
        raise ValidationError(
            f"Phone Number must be exactly 11 numbers in length")


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    phone = StringField(validators=[Required(), reformat_phone])
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='Password must be '
                                                                                   'between 6 and 12'
                                                                                   ' characters in '
                                                                                   'length.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must '
                                                                                         'be equal!')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='PIN Key must be exactly 32 '
                                                                                 'characters in length')])

    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[#?!@$%^&*-])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special "
                                  "character.")


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin_key = StringField(validators=[Required()])
    submit = SubmitField()
