import datetime
import flask
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import  LoginForm, RegisterForm, ManageOnlineShopForm,AddCarForm, CATEGORIAS_LIST,MODA_LIST
from flask_login import login_user
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///online_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
prod_list_glb =[]
prod_list_det_glb =[]
CATEGORIA_DEFAULT_TUPLA =()
MODA_DEFAULT_TUPLA =()
# COMPANY_NAME ='Online clothing store'
COMPANY_NAME ='Fashion Market'
CURRENT_YEAR = datetime.datetime.now().year
USER_CARD_LIST =[]
user_card_toshow_list =[]
full_name_user='Identificate'
# UserMin implementation
class Categories(db.Model, UserMixin):
    __tablename__ = "categories"
    categoria_id     =db.Column(db.Integer,primary_key =True)
    desc_categoria   =db.Column(db.String(50),unique =True,nullable = False)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id          =db.Column(db.Integer,primary_key =True)
    email       =db.Column(db.String(50),unique =True,nullable = False)
    password    =db.Column(db.String(50),nullable = False)
    name        =db.Column(db.String(100),nullable =False)
    telf_contact=db.Column(db.String(20),nullable =False)

class Products_vw(db.Model, UserMixin):
    __viewname__ = "products_vw"
    prod_id         =db.Column(db.Integer,primary_key =True)
    categoria_id    =db.Column(db.Integer, primary_key=False)
    desc_small_prod =db.Column(db.String(100),unique =True,nullable = False)
    desc_large_prod =db.Column(db.String(100),nullable = False)
    img_prod        =db.Column(db.String(100),nullable =False)
    price_prod      =db.Column(db.Float, primary_key=False,nullable = False)
    sex_prod        =db.Column(db.String(1), nullable=False)
    target_prod     =db.Column(db.String(1), nullable=False)
    size_L_count    =db.Column(db.Integer, primary_key=False,nullable = False)
    size_S_count    =db.Column(db.Integer, primary_key=False,nullable = False)
    size_M_count    =db.Column(db.Integer, primary_key=False,nullable = False)
    size_XL_count   =db.Column(db.Integer, primary_key=False,nullable = False)
    size_XXL_count  =db.Column(db.Integer, primary_key=False,nullable = False)
    size_3XL_count  =db.Column(db.Integer, primary_key=False,nullable = False)
    size_XLS_count  =db.Column(db.Integer, primary_key=False,nullable = False)
    total_count = db.Column(db.Integer, primary_key=False, nullable=False)

class Products(db.Model, UserMixin):
    __tablename__ = "products"
    prod_id         =db.Column(db.Integer,primary_key =True)
    categoria_id    =db.Column(db.Integer, primary_key=False)
    desc_small_prod =db.Column(db.String(100),unique =True,nullable = False)
    desc_large_prod =db.Column(db.String(100),nullable = False)
    img_prod        =db.Column(db.String(100),nullable =False)
    price_prod      =db.Column(db.Float, primary_key=False,nullable = False)
    sex_prod        =db.Column(db.String(1), nullable=False)
    target_prod     =db.Column(db.String(1), nullable=False)
    size_L_count    =db.Column(db.Integer, primary_key=False,nullable = False)
    size_S_count    =db.Column(db.Integer, primary_key=False,nullable = False)
    size_M_count    =db.Column(db.Integer, primary_key=False,nullable = False)
    size_XL_count   =db.Column(db.Integer, primary_key=False,nullable = False)
    size_XXL_count  =db.Column(db.Integer, primary_key=False,nullable = False)
    size_3XL_count  =db.Column(db.Integer, primary_key=False,nullable = False)
    size_XLS_count  =db.Column(db.Integer, primary_key=False,nullable = False)

# Inicio Funciones python
def fn_get_car_length():
    global USER_CARD_LIST
    length_car =0
    for prod in USER_CARD_LIST:
        length_car += int(prod[1])
    return length_car

def fn_get_categories(pCategory):
    global CATEGORIAS_LIST,CATEGORIA_DEFAULT_TUPLA
    if not pCategory:
        categories_prod = db.session.query(Categories).all()
        for idx in range(len(categories_prod)):
            CATEGORIAS_LIST.append((categories_prod[idx].categoria_id,categories_prod[idx].desc_categoria))
    else:
        categories_prod = Categories.query.get(pCategory)
        CATEGORIA_DEFAULT_TUPLA =(categories_prod.categoria_id, categories_prod.desc_categoria)

def fn_get_list_products(pTarget,pSize):
    global prod_list_glb

    if pTarget =='All' and pSize =='All':
        prod_list_glb = Products_vw.query.filter(Products_vw.total_count > 0).all()
    else:
        if pSize =='All' :
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget).all()
        elif pSize =='L' :
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget, Products_vw.size_L_count > 0).all()
        elif pSize =='S' :
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget, Products_vw.size_S_count > 0).all()
        elif pSize =='M' :
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget, Products_vw.size_M_count > 0).all()
        elif pSize =='XL' :
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget, Products_vw.size_XL_count > 0).all()
        elif pSize =='XXL' :
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget, Products_vw.size_XXL_count > 0).all()
        elif pSize =='3XL' :
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget, Products_vw.size_3XL_count > 0).all()
        else : # XLS
            prod_list_glb = Products_vw.query.filter(Products_vw.target_prod == pTarget, Products_vw.size_XLS_count > 0).all()

def fn_get_det_products(pProd_id):
    global prod_list_det_glb
    prod_list_det_glb = Products_vw.query.filter(Products_vw.prod_id == pProd_id).all()

def fn_search_products(pTextFilter):
    global prod_list_glb
    prod_list_glb = Products_vw.query.filter(Products_vw.desc_large_prod.like(f"%{pTextFilter}%"), Products_vw.total_count > 0).all()
    if not prod_list_glb:
        prod_list_glb = Products_vw.query.filter(Products_vw.desc_small_prod.like(f"%{pTextFilter}%"),Products_vw.total_count > 0).all()


def fn_update_and_delete_product(pOpType,pProd_id,pUpd_prod_reg):
    product_to_upddel = Products.query.get(pProd_id)
    if pOpType =='D':
        db.session.delete(product_to_upddel)
    else:
         product_to_upddel.categoria_id     = pUpd_prod_reg.categoria_id
         product_to_upddel.desc_small_prod  = pUpd_prod_reg.desc_small_prod
         product_to_upddel.desc_large_prod  = pUpd_prod_reg.desc_large_prod
         product_to_upddel.img_prod         = pUpd_prod_reg.img_prod
         product_to_upddel.price_prod       = pUpd_prod_reg.price_prod
         product_to_upddel.sex_prod         = pUpd_prod_reg.sex_prod
         product_to_upddel.target_prod      = pUpd_prod_reg.target_prod
         product_to_upddel.size_L_count     = pUpd_prod_reg.size_L_count
         product_to_upddel.size_S_count     = pUpd_prod_reg.size_S_count
         product_to_upddel.size_M_count     = pUpd_prod_reg.size_M_count
         product_to_upddel.size_XL_count    = pUpd_prod_reg.size_XL_count
         product_to_upddel.size_XXL_count   = pUpd_prod_reg.size_XXL_count
         product_to_upddel.size_3XL_count   = pUpd_prod_reg.size_3XL_count
         product_to_upddel.size_XLS_count   = pUpd_prod_reg.size_XLS_count
    db.session.commit()
    fn_get_list_products(pTarget='All'
                         , pSize='All')

def fn_get_user_car():
    global USER_CARD_LIST,user_card_toshow_list
    user_card_toshow_list =[]
    for prod in USER_CARD_LIST :
        user_card_toshow_list.append( Products_vw.query.get(int(prod[0])))

# Fin Funciones python
#Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def fn_home():
    global full_name_user
    return render_template(template_name_or_list='index.html'
                           ,company_name        =COMPANY_NAME
                           ,prod_list_shop      =prod_list_glb
                           ,current_year        =CURRENT_YEAR
                           ,full_name_user      =full_name_user
                           ,mycar               =fn_get_car_length()
                           )

@login_manager.user_loader
def fn_load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/fn_login', methods=["GET","POST"])
def fn_login():
    global full_name_user
    form = LoginForm()
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        # Check if the user mail existe
        chk_user_mail = User.query.filter_by(email = user_email).first()
        if chk_user_mail :
            if form.validate_on_submit():
                if check_password_hash(pwhash=chk_user_mail.password,password=user_password):
                    login_user(chk_user_mail)
                    full_name_user = chk_user_mail.email
                    return redirect(location=url_for("fn_home"))
            else:
                flask.flash("Disculpe, Password invalido, por favor intente de nuevo")
                return redirect(location=url_for("fn_login"))
        else:
            flask.flash("Disculpe, Correo invalido, por favor intente de nuevo")
            return redirect(location=url_for("fn_login"))

    return render_template(template_name_or_list='login.html'
                           ,conpany_name        =COMPANY_NAME
                           ,form                =form
                           ,btn_title           ='HOME'
                           ,current_year        =CURRENT_YEAR
                           ,full_name_user     =full_name_user)

@app.route('/fn_logout')
def fn_logout():
    global full_name_user
    full_name_user = 'Identificate'
    logout_user()
    return redirect(url_for('fn_home'))

@app.route('/fn_register', methods=["GET","POST"])
def fn_register():
    form = RegisterForm()
    if request.method == "POST":
       # Check if the user mail existe
       chk_user_mail = User.query.filter_by(email=request.form.get('email')).first()
       if chk_user_mail:
           flask.flash("Disculpe, Este EMAIL ya existe, favor intente de nuevo")
           return redirect(location=url_for("fn_register"))
       else:
           if form.validate_on_submit():
               new_user_reg = User(name    = request.form.get('name')
                                   ,email  = request.form.get('email')
                                   ,password =generate_password_hash(password=request.form.get("password"), method = 'pbkdf2:sha256',salt_length=8)
                                   ,telf_contact=request.form.get('telf_contact')
                                    )
               db.session.add(new_user_reg)
               db.session.commit()
               login_user(new_user_reg)
               return redirect(url_for('fn_home'))
    return render_template(template_name_or_list='register.html'
                            ,conpany_name       =COMPANY_NAME
                            ,form               =form
                            ,btn_title          ='HOME'
                            ,current_year       =CURRENT_YEAR
                            ,full_name_user     =full_name_user
                           )

@app.route('/fn_apply_filters', methods=["GET","POST"])
def fn_apply_filters():
    fn_get_list_products(pTarget=request.values.get("chk_sexo")
                         ,pSize= request.values.get("chk_size"))
    return redirect(url_for('fn_home'))

@app.route('/fn_search', methods=["GET","POST"])
def fn_search():
    fn_search_products(pTextFilter=request.values.get("inp_search"))
    return redirect(url_for('fn_home'))

@app.route('/fn_show_product/<prod_id>',methods=["GET","POST"])
def fn_show_product(prod_id):
    global prod_list_det_glb,USER_CARD_LIST
    form = AddCarForm()
    if request.method =='POST':
        USER_CARD_LIST.append((prod_id,request.form.get('cantidad_req')))
        return redirect(url_for('fn_home'))
    else:
        fn_get_det_products(pProd_id=prod_id)
        return render_template(template_name_or_list='show-prod.html'
                               ,conpany_name        =COMPANY_NAME
                               ,btn_title           ='HOME'
                               ,current_year        =CURRENT_YEAR
                               ,prod_list_det       =prod_list_det_glb
                               ,full_name_user      =full_name_user
                               ,form                =form
                               )

#Mark with decorator
@app.route("/fn_manage_onlineshop",methods=["GET","POST"])
@admin_only
def fn_manage_onlineshop():
    form = ManageOnlineShopForm()
    if request.method == "POST":
        if request.form.get('target_prod') in ['Mujer','Niña']:
            sex_prod ='F'
        else:
            sex_prod = 'M'
        new_prod_reg = Products(categoria_id        =request.form.get('categoria')
                                ,desc_small_prod    =request.form.get('desc_small_prod')
                                ,desc_large_prod    =request.form.get('desc_large_prod')
                                ,img_prod           =request.form.get('img_prod')
                                ,price_prod         =float(request.form.get('price_prod').replace(',','.'))
                                ,sex_prod           =sex_prod
                                ,target_prod        =request.form.get('target_prod')
                                ,size_L_count       =request.form.get('size_L_count')
                                ,size_S_count       =request.form.get('size_S_count')
                                ,size_M_count       =request.form.get('size_M_count')
                                ,size_XL_count      =request.form.get('size_XL_count')
                                ,size_XXL_count     =request.form.get('size_XXL_count')
                                ,size_3XL_count     =request.form.get('size_3XL_count')
                                ,size_XLS_count     =request.form.get('size_XLS_count')
                                )
        db.session.add(new_prod_reg)
        db.session.commit()

    return render_template(template_name_or_list='manage-prod.html'
                           ,conpany_name       =COMPANY_NAME
                           ,btn_title          ='HOME'
                           ,current_year       =CURRENT_YEAR
                           ,form                = form
                           ,full_name_user      =full_name_user
                           ,CATEGORIAS_LIST     =CATEGORIAS_LIST
                           )

@app.route("/fn_manage_one_product/<prod_id>'",methods=["GET","POST"])
@admin_only
def fn_manage_one_product(prod_id):
    global prod_list_det_glb, CATEGORIA_DEFAULT_TUPLA,CATEGORIAS_LIST,MODA_LIST,MODA_DEFAULT_TUPLA
    form = ManageOnlineShopForm()
    # print(request.form.get('desc_small_prod'))
    # print(request.form.get('submit_upd'))
    # print(request.form.get('submit_del'))
    if request.form.get('submit_upd') ==None and request.form.get('submit_del') ==None:
        # print('MOSTRANDO REGISTRO')
        # print(prod_id)
        fn_get_det_products(pProd_id=prod_id)
        fn_get_categories(pCategory=prod_list_det_glb[0].categoria_id)
        # print(prod_list_det_glb[0].categoria_id)
        # print(CATEGORIA_DEFAULT_TUPLA)
        CATEGORIAS_LIST.remove(CATEGORIA_DEFAULT_TUPLA)
        CATEGORIAS_LIST.insert(0,CATEGORIA_DEFAULT_TUPLA)
        # print(CATEGORIAS_LIST)
        MODA_DEFAULT_TUPLA =(prod_list_det_glb[0].target_prod,f'Moda para {prod_list_det_glb[0].target_prod}')
        MODA_LIST.remove(MODA_DEFAULT_TUPLA)
        MODA_LIST.insert(0,MODA_DEFAULT_TUPLA)
        form = ManageOnlineShopForm()
        return render_template(template_name_or_list='show-prod-manage.html'
                               , conpany_name=COMPANY_NAME
                               , btn_title='HOME'
                               , current_year=CURRENT_YEAR
                               , form=form
                               , full_name_user=full_name_user
                               , CATEGORIAS_LIST=CATEGORIAS_LIST
                               , prod_list_det=prod_list_det_glb
                               , categoria_default=CATEGORIA_DEFAULT_TUPLA
                               )
    elif request.form.get('submit_upd') ==None and request.form.get('submit_del') =='Borrar':
        fn_update_and_delete_product(pOpType='D', pProd_id=prod_id,pUpd_prod_reg=None)
    elif request.form.get('submit_upd') =='Actualizar' and request.form.get('submit_del') ==None:
        form = ManageOnlineShopForm()
        if request.form.get('target_prod') in ['Mujer', 'Niña']:
            sex_prod = 'F'
        else:
            sex_prod = 'M'
        upd_prod_reg = Products(categoria_id       =request.form.get('categoria')
                                ,desc_small_prod   =request.form.get('desc_small_prod')
                                ,desc_large_prod   =request.form.get('desc_large_prod')
                                ,img_prod          =request.form.get('img_prod')
                                ,price_prod        =float(request.form.get('price_prod').replace(',','.'))
                                ,sex_prod          =sex_prod
                                ,target_prod       =request.form.get('target_prod')
                                ,size_L_count      =request.form.get('size_L_count')
                                ,size_S_count      =request.form.get('size_S_count')
                                ,size_M_count      =request.form.get('size_M_count')
                                ,size_XL_count     =request.form.get('size_XL_count')
                                ,size_XXL_count    =request.form.get('size_XXL_count')
                                ,size_3XL_count    =request.form.get('size_3XL_count')
                                ,size_XLS_count    =request.form.get('size_XLS_count')
                                )
        fn_update_and_delete_product(pOpType='U', pProd_id=prod_id,pUpd_prod_reg=upd_prod_reg)

    return redirect(url_for('fn_home'))

@app.route("/fn_show_user_card",methods=["GET","POST"])
def fn_show_user_card():
    global full_name_user,user_card_toshow_list,COMPANY_NAME
    fn_get_user_car()
    return render_template(template_name_or_list    ='show_user_car.html'
                           ,btn_title               ='HOME'
                           , conpany_name=COMPANY_NAME
                           ,current_year            =CURRENT_YEAR
                           ,full_name_user          =full_name_user
                           ,user_card_toshow_list   =user_card_toshow_list
                           )
fn_get_categories(pCategory='')
fn_get_list_products(pTarget='All'
                         ,pSize='All')
if __name__ == '__main__':
    # fn_get_categories(pCategory='')
    # fn_get_list_products(pTarget='All'
    #                      ,pSize='All')
    app.run(debug=True,port=5001)
