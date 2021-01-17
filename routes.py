from app import app, db
from flask import request, render_template, flash, redirect, url_for
from models import Country, Gold, Sport
from forms import SearchForm, SearchResults
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
def index(): 
    field = request.args.get('field')
    sort = request.args.get('sort')
    name = request.args.get('name')
    country = Country.query.filter_by(name=name).first()
    if field == 'gdp':
        order = Country.gdp
    elif field == 'population':
        order = Country.population
    elif field == 'medals':
        order = Country.medals
    else:
        order = Country.name
    if sort == 'desc':
        countries = Country.query.order_by(order.desc()).all()
    elif sort == 'solo':
        countries = []
    else:
        countries = Country.query.order_by(order.asc()).all()
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data.lower().title()
        country = Country.query.filter_by(name=name).first()
        if country is None:
            flash('Check your spelling')
            return redirect(url_for('index'))
        elif country.medals == 0:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index', sort='solo', name=name)
            return redirect(next_page)
        else:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('metrics', new_country=name)
            return redirect(next_page)
    return render_template('landing_page.html', country=country, countries=countries, form=form)


@app.route('/<new_country>/gold_medal_list', methods=['GET', 'POST'])
def metrics(new_country):
    field = request.args.get('field')
    sort = request.args.get('sort')
    country = Country.query.filter_by(name=new_country).first()
    if field == 'season':
        order = Gold.season
    elif field == 'city':
        order = Gold.city
    elif field == 'name':
        order = Gold.name
    elif field == 'event':
        order = Gold.event
    else:
        order = Gold.year
    if sort == 'asc':
        golds = Gold.query.filter_by(country_id=country.id).order_by(order.asc()).all()
    else:
        golds = Gold.query.filter_by(country_id=country.id).order_by(order.desc()).all()
    results = SearchResults()
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data.lower().title()
        country = Country.query.filter_by(name=name).first()
        if country is None:
            flash('Check your spelling')
            return redirect(url_for('index'))
        elif country.medals == 0:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index', field='solo', sort='solo', name=name)
            return redirect(next_page)
        else:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('metrics', new_country=name)
            return redirect(next_page)
    return render_template('metrics.html', country=country, golds=golds, form=form, results=results)


@app.route('/<new_country>/sports_list', methods=['GET', 'POST'])
def sports(new_country):
    field = request.args.get('field')
    sort = request.args.get('sort')
    country = Country.query.filter_by(name=new_country).first()
    if field == 'name':
        order = Sport.name
    elif field == 'percent':
        order = Sport.percent
    else:
        order = Sport.count
    if sort == 'asc':
        sports = Sport.query.filter_by(country_id=country.id).order_by(order.asc()).all()
    else:
        sports = Sport.query.filter_by(country_id=country.id).order_by(order.desc()).all()
    results = SearchResults()
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data.lower().title()
        country = Country.query.filter_by(name=name).first()
        if country is None:
            flash('Check your spelling')
            return redirect(url_for('index'))
        elif country.medals == 0:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index', field='solo', sort='solo', name=name)
            return redirect(next_page)
        else:
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('sports', new_country=name)
            return redirect(next_page)
    return render_template('sports.html', country=country, sports=sports, form=form, results=results)
