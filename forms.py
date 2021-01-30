from wtforms import Form, StringField, TextAreaField, PasswordField, validators


class RegisterForm(Form):
    name = StringField('Name', validators=[validators.Length(min=2, max=50)])
    username = StringField('Username', validators=[validators.Length(min=6, max=30)])
    email = StringField('Email', validators=[validators.Length(min=8, max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match'),
        validators.Length(min=8, max=50)
    ])
    confirm = PasswordField('Confirm password')