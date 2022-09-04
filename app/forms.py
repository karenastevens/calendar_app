from wtforms.fields import (BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField)
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import (DataRequired, ValidationError)

class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('Start', validators=[DataRequired()])
    start_time = TimeField('Start', validators=[DataRequired()])
    end_date = DateField('End', validators=[DataRequired()])
    end_time = TimeField('End', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    private = BooleanField('Private?')
    submit = SubmitField('Create appointment')

    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(form.end_date.data, form.end_time.data)

        if start >= end:
            raise ValidationError('End date/time must come after start date/time')
        if form.start_date.data != form.end_date.data:
            raise ValidationError('Start and end date must be the same')
