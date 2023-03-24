from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import User
from . import db, userDataStore
import logging

auth = Blueprint('auth', __name__, url_prefix='/security')

@auth.route('/login')
def login():
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logging.info('ACCESO AL MODULO DE LOGIN')
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('El usuario y/o la contraseña son incorrectos')
        logging.basicConfig(filename='logs.log', level=logging.WARNING)
        logging.error('INICIO DE SESION FALLIDO')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logging.info('INICIO DE SESION')
    return redirect(url_for('main.galeria'))

@auth.route('/register')
def register():
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logging.info('ACCESO AL MODULO DE REGISTRO')
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        flash('El correo electrónico ya existe')
        logging.basicConfig(filename='logs.log', level=logging.WARNING)
        logging.warning('PETICION DE UN CORREO YA EXISTENTE')
        return redirect(url_for('auth.register'))
    userDataStore.create_user(
        name=name, email=email, password=generate_password_hash(password, method='sha256')
    )
    db.session.commit()
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logging.info('REGISTRO DE UN NUEVO USUARIO')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logging.info('CERRAR SESION')
    return redirect(url_for('main.index'))

@auth.route('/contacto')
def contactos():
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logging.info('ACCESO AL MODULO DE CONTACTO')
    return render_template('contactos.html')

