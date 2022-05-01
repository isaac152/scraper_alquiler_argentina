#Python imports
import random

#External imports
from flask import jsonify, render_template, session,request,flash,redirect,url_for
import numpy as np
#Local imports
from . import app
from utils import get_data
from app.utils import get_neighborhoods,get_apartaments_by_neighborhood,get_best_apartaments_m2_price
from app.utils import get_cheaper_apartaments_per_m2


@app.route('/')
def index():
    data = get_data()
    choices = np.random.choice(data,size=3,replace=False)
    neighborhoods = get_neighborhoods(data)
    return render_template(
        'index.html',
        apartaments = choices,
        neighborhoods = neighborhoods
        )
@app.route('/comparador_submit',methods=['POST'])
def comparator_submit():
    neighborhood = request.form['neighborhood']
    return redirect(url_for('comparator',neighborhood=neighborhood))


@app.route('/comparador/<neighborhood>')
def comparator(neighborhood):
    data = get_data()
    apartaments_filtred = get_apartaments_by_neighborhood(data,neighborhood)
    apartaments_m2_price = get_best_apartaments_m2_price(apartaments_filtred)
    cheapers_apartaments = get_cheaper_apartaments_per_m2(apartaments_filtred)

    return render_template(
        'comparador.html',
        m2_price = apartaments_m2_price,
        cheapers = cheapers_apartaments
    )
@app.route('/all')
@app.route('/all/<neighborhood>')
def all_apartaments(neighborhood=None):
    data = get_data()
    if neighborhood:
        data = get_apartaments_by_neighborhood(data,neighborhood)
    
    return render_template(
        'listado.html',
        neighborhood=neighborhood,
        apartaments = data
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404