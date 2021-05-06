from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user

from models import get_db, User, Entrada

from module002.forms import *

module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module002.route('/')
@login_required
def module002_index():
    if current_user.profile in ('admin','staff','student'):
        return render_template("module002_index.html",module="module002")
    else:
        flash("Access denied!")
#        abort(404,description="Access denied!")
        return redirect(url_for('index'))


@module002.route('/crear_entrada', methods=['GET','POST'])
@login_required
def module002_crear_entrada():
    form = EntradaForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            entrada = Entrada(titulo=form.titulo.data, cuerpo = form.cuerpo.data,user_id=current_user.id)
            db.session.add(entrada)
            try:
                db.session.commit()
                flash("Todo guay")
            except:
                db.session.rollback()
                flash("Error in database!")
        return redirect(url_for('module001.module001_index'))
    else:
        if current_user.profile in ('admin','staff','student'):
            return render_template("module002_crear_entrada.html",module="module002",form=form)
        else:
            flash("Access denied!")
    #       abort(404,description="Access denied!")
            return redirect(url_for('index'))


@module002.route('/test')
def module002_test():
    return 'OK'
