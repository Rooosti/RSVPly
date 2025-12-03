from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from datetime import datetime
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from app.models import Category

class EventForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField("Description", validators=[Optional()])
    wishlist = TextAreaField("Wishlist", validators=[Optional()])

    starts_at = DateTimeLocalField("Starts at", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    ends_at = DateTimeLocalField("Ends at", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    capacity = IntegerField("Capacity",validators=[Optional(), NumberRange(min=1)])
    is_public = BooleanField("Public?", default=True)
    address_line1 = StringField("Address line 1", validators=[DataRequired(), Length(max=255)])
    address_line2 = StringField("Address line 2", validators=[Optional(), Length(max=255)])

    categories = QuerySelectMultipleField(
        "Categories",
        query_factory=lambda: Category.query.order_by(Category.name).all(),
        get_label="name"
    )

    submit = SubmitField("Create Event")

    def validate_ends_at(self, field):
        if self.starts_at.data and field.data and field.data <= self.starts_at.data:
            raise ValidationError("End time must be after start time.")

class RegistrationForm(FlaskForm): # form for user registration
    full_name = StringField('Full Name', validators=[validators.DataRequired(), Length(max=255)])
    username = StringField('Username', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.Length(min=4, max=35)])
    remember_me = BooleanField("Remember Me")
    submit =  SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit =  SubmitField("Login")

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[validators.DataRequired()])
    submit =  SubmitField("Submit Comment")


class RatingForm(FlaskForm):
    score = IntegerField('Rate (1-5)', validators=[validators.DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField("Submit Rating")

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    submit =  SubmitField("Apply")

class EditEventForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField("Description", validators=[Optional()])
    wishlist = TextAreaField("Wishlist", validators=[Optional()])

    starts_at = DateTimeLocalField("Starts at", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    ends_at = DateTimeLocalField("Ends at", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    capacity = IntegerField("Capacity",validators=[Optional(), NumberRange(min=1)])
    is_public = BooleanField("Public?", default=True)
    address_line1 = StringField("Address line 1", validators=[DataRequired(), Length(max=255)])
    address_line2 = StringField("Address line 2", validators=[Optional(), Length(max=255)])

    categories = QuerySelectMultipleField(
        "Categories",
        query_factory=lambda: Category.query.order_by(Category.name).all(),
        get_label="name"
    )

    submit = SubmitField("Apply Changes")

    def validate_ends_at(self, field):
        if self.starts_at.data and field.data and field.data <= self.starts_at.data:
            raise ValidationError("End time must be after start time.")

class SearchForm(FlaskForm):
    search_query= StringField('Search', validators=[validators.Optional()])
    submit = SubmitField('Search')

class EnhancedSearchForm(FlaskForm):
    search_query = StringField('Search', validators=[validators.Optional()])
    tags = StringField('Tags (comma-separated)', validators=[validators.Optional()])
    submit = SubmitField('Enhanced Search')
