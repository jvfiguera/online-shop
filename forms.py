from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, FloatField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, length, Length ,input_required,number_range
from flask_ckeditor import CKEditorField

CATEGORIAS_LIST =[]
MODA_LIST       =[('Mujer','Moda para Mujer'),('Niñas','Moda para Niñas'),('Hombres','Moda para Hombres'),('Niños','Moda para Niños')]
# Flask Form
class LoginForm(FlaskForm):
    email       = StringField("Email", validators=[DataRequired(), length(min=10 , max=40), input_required()])
    password    = PasswordField("Password",validators=[DataRequired(),length(min=10, max=40),input_required()])
    submit      = SubmitField("Login")

class RegisterForm(FlaskForm):
    name        = StringField('Nombre Completo:',[DataRequired(),length(min=20, max=100),input_required()])
    email       = StringField("Email:", validators=[DataRequired(), length(min=10 , max=40),input_required()])
    password    = PasswordField("Password:",validators=[DataRequired(),length(min=10, max=40),input_required()])
    telf_contact = StringField("Telf. Contacto", validators=[DataRequired(), length(min=10, max=40), input_required()])
    submit      = SubmitField("Register")

class ManageOnlineShopForm(FlaskForm):
    prod_id         =IntegerField('Identificador del producto  :',[DataRequired(),length(min=1, max=3),input_required()], default=0)
    categoria       =SelectField('Categoria                    :',[DataRequired(),length(min=10, max=20),input_required()],coerce=str, choices=CATEGORIAS_LIST)
    desc_small_prod =StringField('Descripcion Corta            :',[DataRequired(),length(min=5, max=20),input_required()])
    desc_large_prod =StringField('Descripcion Larga            :',[DataRequired(),length(min=5, max=100),input_required()])
    img_prod        =StringField('Nombre del archivo imagen    :',[DataRequired(),length(min=5, max=50),input_required()])
    price_prod      =FloatField ('Precio del producto          :',[DataRequired(),length(min=1, max=5),input_required()], default=0)
    sex_prod        =SelectField('Tipo de prenda               :',[DataRequired(),length(min=1, max=1),input_required()],coerce=str, choices=[('F','Femenino'),('M','Masculina')])
    target_prod     =SelectField('Público destino              :',[DataRequired(),length(min=10, max=20),input_required(),number_range(min=0, max=5)],coerce=str, choices=MODA_LIST)
    size_L_count    =IntegerField('Cantidad existente talla L  :',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)], default=0)
    size_S_count    =IntegerField('Cantidad existente talla S  :',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)], default=0)
    size_M_count    =IntegerField('Cantidad existente talla L  :',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)], default=0)
    size_XL_count   =IntegerField('Cantidad existente talla XL :',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)],default=0)
    size_XXL_count  =IntegerField('Cantidad existente talla XXL:',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)],default=0)
    size_3XL_count  =IntegerField('Cantidad existente talla 3XL:',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)],default=0)
    size_XLS_count  =IntegerField('Cantidad existente talla XLS:',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)],default=0)
    submit          = SubmitField("Guardar")
    submit_upd      = SubmitField("Actualizar")
    submit_del      = SubmitField("Borrar")

class AddCarForm(FlaskForm):
    cantidad_req   =IntegerField('Cantidad:',[DataRequired(),length(min=1, max=3),input_required(),number_range(min=0, max=5)], default=0)
    submit         =SubmitField("Carrito")
