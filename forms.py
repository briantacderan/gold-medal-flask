from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from models import Country, Gold
from app import app, db

import numpy as np
import pandas as pd
from sqlalchemy import asc, desc, func, distinct, column, sql

from werkzeug.urls import url_parse



class SearchForm(FlaskForm):
    name = StringField('Country name', validators=[DataRequired('Search for a country')])
    submit = SubmitField('SEARCH')
    
    
    def validate_country(self, name):
        country = Country.query.filter_by(name=name.data).first()
        if country is None:
            raise ValidationError('Invalid country name')
    
    
    
class SearchResults(FlaskForm):
    def best_season(self, country, season):
        try:
            year, gold_medals = db.session.query(Gold.year, func.count(Gold.year))\
                                  .filter_by(country=country, season=season)\
                                  .group_by(Gold.year).order_by(func.count(Gold.year)\
                                  .desc()).limit(1)[0]
            string = f'{year} ({gold_medals} medals)'
        except:
            string = '-'
        return string

    
    def best_category(self, country, category):
        if category == 'discipline':
            column = Gold.discipline
        elif category == 'sport':
            column = Gold.sport
        elif category == 'event':
            column = Gold.event
        elif category == 'year':
            column = Gold.year
        category, gold_medals = db.session.query(column, \
                                     func.count(column)).filter_by(country=country)\
                                     .group_by(column)\
                                     .order_by(func.count(column).desc()).limit(1)[0]
        return f'{category} ({gold_medals} medals)'

    
    def gender_metrics(self, country, gender):
        num_gender = db.session.query(distinct(Gold.name)).filter_by(country=country, \
                               gender=gender).count()
        return num_gender

    
    def best_athlete(self, country):
        best = db.session.query(Gold.name, func.count(Gold.name))\
                            .filter_by(country=country).group_by(Gold.name)\
                            .order_by(func.count(Gold.name).desc()).limit(1)[0][0]
        [last, first] = best.split(', ')
        olympia = f'{first} {last.lower().title()}'
        return olympia
