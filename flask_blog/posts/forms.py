from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    picture = FileField('Приложите фото к посту', validators=[FileAllowed(['jpg', 'png'])])


class CommentForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])


class LikeForm(FlaskForm):
    submit = SubmitField('Создать')
