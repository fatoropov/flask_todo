from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    SubmitField,
    TextAreaField,
    HiddenField,
    validators,
)


class AddForm(FlaskForm):
    title = StringField("Задача",
                        validators=[validators.DataRequired(),
                                    validators.Length(max=140)])
    desc = TextAreaField("Описание",
                         validators=[validators.Length(min=0, max=500)])
    deadline = DateField('Дедлайн', format='%Y-%m-%d')
    time_offset = HiddenField("time_offset")
    submit = SubmitField("Сохранить")
