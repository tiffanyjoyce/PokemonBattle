from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    img_url = StringField('Image URL')
    body = StringField('Body')
    submit = SubmitField()

class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    img_url = StringField('Image URL')
    body = StringField('Body')
    submit = SubmitField()




