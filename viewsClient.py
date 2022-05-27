from itertools import count
from flask import Blueprint, jsonify, render_template, request, flash, jsonify, redirect, url_for, request, Response
from .models import Service
from .models import Gallery
import numpy as np
viewsClient = Blueprint('viewsClient', __name__)

@viewsClient.route('/')
def home():
    result = Service.query.all()
    return render_template('client/home.html', data = result)

@viewsClient.route('/about')
def about():
    return render_template('client/about.html')

@viewsClient.route('/services')
def services():
    result = Service.query.all()
    if len(result) % 4 == 0:
        number = len(result) / 4
    else:
        number = len(result) // 4 + 1
    new_result = np.array_split(result, number)
    return render_template('client/services.html', data = new_result)

@viewsClient.route('/gallery')
def gallery():
    result = Gallery.query.all()
    return render_template('client/gallery.html', data = result)

@viewsClient.route('/contact')
def contact():
    return render_template('client/contact.html')

@viewsClient.route('/admin')
def admin():
    return render_template('admin/login.html')

@viewsClient.route('/face_detection')
def face_detection():
    return render_template('client/face_detection.html')