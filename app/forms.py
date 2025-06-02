from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-posta', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Şifre Tekrar', validators=[DataRequired(), EqualTo('password')])

class PostForm(FlaskForm):
    title = StringField('Başlık', validators=[DataRequired(), Length(min=3, max=100)])
    content = TextAreaField('İçerik', validators=[DataRequired()])
    category = SelectField('Kategori', choices=[
        ('teknoloji', 'Teknoloji'),
        ('yazilim', 'Yazılım'),
        ('tasarim', 'Tasarım'),
        ('diger', 'Diğer')
    ])
    tags = StringField('Etiketler', validators=[Optional()])
    cover_image = FileField('Kapak Fotoğrafı', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim dosyaları yükleyebilirsiniz!')
    ])
    is_published = BooleanField('Yayınla', default=True) 