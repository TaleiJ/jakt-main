from secrets import choice
from tokenize import String
from xmlrpc.client import DateTime
from wtforms import widgets
from wtforms.fields.core import Field
from flask import Flask
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, SelectField, DateField, DateTimeField, PasswordField, IntegerField, RadioField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.widgets import HiddenInput
import datetime

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

class TimeField(DateTimeField):
    widget = widgets.TimeInput()
    def __init__(self, label=None, validators=None, format="%H:%M", **kwargs):
        super().__init__(label, validators, format, **kwargs)

    def process_formdata(self, valuelist):
        if not valuelist:
            return
        time_str = " ".join(valuelist)
        try:
            self.data = datetime.datetime.strptime(
                time_str, "%H:%M"
            ).time()
        except ValueError as exc:
            self.data = None
            raise ValueError(self.gettext("Not a valid time value.")) from exc

#Creates new event
class EventForm(FlaskForm):
    name = StringField('Event Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[FileRequired(message='Image Upload Required'), 
                                                 FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, PNG, JPG')])
    genre = SelectField('Genre', validators=[InputRequired()], choices=['Pop', 'Rock', 'Jazz', 'Country', 'Electronic', 'Metal'])
    venue = StringField('Venue', validators=[InputRequired()])
    date = DateField('Event Date', validators=[InputRequired()])
    start_time = TimeField('Start time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    price = IntegerField('Ticket Price', validators=[InputRequired()])
    tickets = IntegerField('Number of Available Tickets', validators=[InputRequired()])
    status = SelectField('Event Status', validators=[InputRequired()], choices=['Open', 'Unpublished', 'Sold-out', 'Cancelled'])
    submit = SubmitField("Create")
    name = StringField('Event Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('Event Image', validators=[FileRequired(message='Image Upload Required'), 
                                                 FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, PNG, JPG')])
    genre = SelectField('Genre', validators=[InputRequired()], choices=['Pop', 'Rock', 'Jazz', 'Country', 'Electronic', 'Metal'])
    venue = StringField('Venue', validators=[InputRequired()])
    date = DateField('Event Date', validators=[InputRequired()])
    start_time = TimeField('Start time', validators=[InputRequired()])
    end_time = TimeField('End Time', validators=[InputRequired()])
    price = IntegerField('Ticket Price', validators=[InputRequired()])
    tickets = IntegerField('Number of Available Tickets', validators=[InputRequired()])
    status = SelectField('Event Status', validators=[InputRequired()], choices=['Open', 'Unpublished', 'Sold-out', 'Cancelled'])
    submit = SubmitField("Create")

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact_num = IntegerField("Contact Number", validators=[InputRequired(message="Please enter a valid Phone Number")])
    streetAddress = StringField("Street Address", validators=[InputRequired()])

    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')

#ticket handling
class TicketForm(FlaskForm):
  tickets = SelectField('Ticket Number', validators=[InputRequired()], choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
  submit2 = SubmitField('Purchase Tickets')

#delete event
class EditForm(FlaskForm):
  name = StringField('Event Title', validators=[InputRequired()])
  description = TextAreaField('Description', validators=[InputRequired()])
  image = FileField('Event Image', validators=[FileRequired(message='Image Upload Required'), 
                                               FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, PNG, JPG')])
  genre = SelectField('Genre', validators=[InputRequired()], choices=['Pop', 'Rock', 'Jazz', 'Country', 'Electronic', 'Metal'])
  venue = StringField('Venue', validators=[InputRequired()])
  date = DateField('Event Date', validators=[InputRequired()])
  start_time = TimeField('Start time', validators=[InputRequired()])
  end_time = TimeField('End Time', validators=[InputRequired()])
  price = IntegerField('Ticket Price', validators=[InputRequired()])
  tickets = IntegerField('Number of Available Tickets', validators=[InputRequired()])
  status = SelectField('Event Status', validators=[InputRequired()], choices=['Open', 'Unpublished', 'Sold-out', 'Cancelled'])
  submit = SubmitField('Update')
  delete = SubmitField('Delete')
