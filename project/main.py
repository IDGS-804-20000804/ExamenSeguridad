import os
import uuid
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_security import login_required, current_user
from flask_security.decorators import roles_required
from project.models import Role, productos
from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main',__name__)

@main.route('/')
def index():
    products = productos.query.all()
    tamanio = len(list(products))
    return render_template('index.html', productos = products, tamanio = tamanio )

@main.route('/administrador')
@login_required
@roles_required('admin')
def admin():
    products = productos.query.all()
    return render_template('productosCRUD.html', productos = products )

@main.route('/administrador', methods=['POST'])
@login_required
def admin_post():
    products = productos.query.all()
    nombre = request.form.get('txtNombre')
    descripcion = request.form.get('txtDescripcion')
    precio = request.form.get('txtPrecio')
    new_producto = productos(nombre, descripcion, precio)
    db.session.add(new_producto)
    db.session.commit()
    flash('El producto se guardo correctamente')
    return redirect(url_for('main.admin'))

@main.route('/delete/<id>')
@login_required
def delete(id):
    producto = productos.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    flash('El producto se eliminó correctamente')
    return redirect(url_for('main.admin'))

@main.route('/update/<id>')
@login_required
def update(id):
    producto=productos.query.get(id)
    print(producto.id)
    return render_template('productosCRUD.html',
                           nombre=producto.name,
                           precio=int(producto.precio),
                           descripcion=str(producto.description),
                           update=True,
                           id=producto.id)
   
@main.route('/updateCom/<id>',methods=['POST'])
@login_required
def updateComfim(id):
    idproducto=id
    producto = productos.query.get(idproducto)
    producto.name = request.form.get('txtNombre')
    producto.description = request.form.get('txtDescripcion')
    producto.precio = request.form.get('txtPrecio')
    db.session.commit()  
    flash('El producto se modifico correctamente')
    return redirect(url_for('main.admin'))
   
@main.route('/administrador')
@login_required
def galeria():
    products = productos.query.all()
    if len( products )==0:
       products = 0
    print(current_user.admin)
    return render_template('galeria.html', productos = products )
