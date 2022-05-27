from fileinput import filename
import os
from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, jsonify, redirect, url_for, request, Response
from flask_login import login_required, current_user
from .models import Service
from .models import Gallery
from sqlalchemy import select
import json
from . import create_app, db
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

viewsAdmin = Blueprint('viewsAdmin', __name__)

@viewsAdmin.route('/admin')
@login_required
def home():
    return render_template('admin/home.html')


@viewsAdmin.route('/admin/service/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        image = request.files['image_file']
        if not image:
            return 'No img upload', 400 
        filename = secure_filename(image.filename)
        app = create_app()
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mimetype = image.mimetype
        name = request.form.get('name')
        # image = request.form.get('image_file')
        description = request.form.get('description')
        new_service = Service(name=name, description= description, mimetype=mimetype, name_img = filename)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('viewsAdmin.list'))
    return render_template('admin/add_service.html')


@viewsAdmin.route('/admin/service/list', methods=['GET', 'POST'])
@login_required 
def list():
    result = Service.query.all()
    return render_template('admin/list_service.html', data = result)

@viewsAdmin.route('/admin/service/delete/<id>', methods=['GET', 'POST'])
@login_required 
def delete(id):
    service = Service.query.filter_by(id=id).first()
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('viewsAdmin.list'))

@viewsAdmin.route('/admin/service/detail/<id>', methods=['GET', 'POST'])
@login_required 
def detail(id):
    gallery_id = Service.query.filter_by(id=id).first()
    if request.method == 'POST':
        if (request.files['image_file']):
            new_image = request.files['image_file']
            new_filename = secure_filename(new_image.filename)
            app = create_app()
            new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            new_mimetype = new_image.mimetype
        else:
            new_filename = gallery_id.name_img
            new_mimetype = gallery_id.mimetype

        new_name = request.form.get('name')
        new_desc = request.form.get('description')
        gallery_id.name = new_name
        gallery_id.description = new_desc
        gallery_id.name_img = new_filename
        gallery_id.mimetype = new_mimetype
        db.session.add(gallery_id)
        db.session.commit()
        return redirect(url_for('viewsAdmin.list'))
    return render_template('admin/detail_service.html', data = gallery_id)

@viewsAdmin.route('/admin/gallery/add', methods=['GET', 'POST'])
@login_required
def add_gallery():
    if request.method == 'POST':
        image = request.files['image_file']
        if not image:
            return 'No img upload', 400 
        filename = secure_filename(image.filename)
        app = create_app()
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mimetype = image.mimetype
        name = request.form.get('name')
        category = request.form.get('category')
        new_gallery = Gallery(name=name, mimetype=mimetype, img = filename, category = category)
        db.session.add(new_gallery)
        db.session.commit()
        return redirect(url_for('viewsAdmin.list_gallery'))
    return render_template('admin/add_gallery.html')

@viewsAdmin.route('/admin/gallery/list', methods=['GET', 'POST'])
@login_required 
def list_gallery():
    result = Gallery.query.all()
    return render_template('admin/list_gallery.html', data = result)

@viewsAdmin.route('/admin/gallery/delete/<id>', methods=['GET', 'POST'])
@login_required 
def delete_gallery(id):
    service = Gallery.query.filter_by(id=id).first()
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('viewsAdmin.list_gallery'))

@viewsAdmin.route('/admin/gallery/edit/<id>', methods=['GET', 'POST'])
@login_required 
def edit_gallery(id):
    gallery_id = Gallery.query.filter_by(id=id).first()
    if request.method == 'POST':
        if (request.files['image_file']):
            new_image = request.files['image_file']
            new_filename = secure_filename(new_image.filename)
            app = create_app()
            new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            new_mimetype = new_image.mimetype
        else:
            new_filename = gallery_id.img
            new_mimetype = gallery_id.mimetype

        new_name = request.form.get('name')
        new_category = request.form.get('category')
        gallery_id.name = new_name
        gallery_id.category = new_category
        gallery_id.img = new_filename
        gallery_id.mimetype = new_mimetype
        db.session.add(gallery_id)
        db.session.commit()
        return redirect(url_for('viewsAdmin.list_gallery'))
    return render_template('admin/edit_gallery.html', data = gallery_id)