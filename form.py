from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, Length

# ürün kayıt formu
class AddProduct(FlaskForm):
  name = StringField("Product Name :",validators=[DataRequired()])
  price = FloatField("Product Price :",validators=[DataRequired()])
  category = SelectField(label="Product Category :", choices=[("phones", "Phone"),("cameras", "Camera"), ("computers", "Computer")])
  picture_link = StringField("Product Picture :",validators=[DataRequired()])
  email = StringField("Enter Your Email :", validators=[Email()] )

  submit = SubmitField("Add")

# Kullanıcı kayıt formu
class RegisterForm(FlaskForm):
  username = StringField("Username :",validators=[DataRequired()])
  email = StringField("Email Address :", validators=[Email()] )
  password = PasswordField("Password :",validators=[DataRequired(), Length(min=4, max=12)])

  submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
  username = StringField("Username :",validators=[DataRequired()])
  password = PasswordField("Password :",validators=[DataRequired(), Length(min=4, max=12)])

  submit = SubmitField("Login")  