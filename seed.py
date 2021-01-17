import numpy as np
import pandas as pd
from app import db
from models import Country, Gold, Sport
import os
from sqlalchemy import distinct


if os.path.exists('gold_medals.db'):
    os.remove('gold_medals.db')
db.create_all()


country_table = pd.read_csv('static/resources/data/country.csv')
gold_table = pd.read_csv('static/resources/data/goldmedal.csv')


for i in range(len(country_table)):
    row = country_table.iloc[i]
    row_array = []
    for j in range(len(row)):
        row_array.append(row[j])
    post_array = Country(name=row_array[0], 
                         code=row_array[1],
                         population=row_array[2],
                         gdp='${0:,.2f}'.format(row_array[3]),
                         medals=0)
    db.session.add(post_array)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()


no_rep_id = len(country_table) + 1     
no_rep = Country(name='Unrepresented',
                 code='UNR',
                 gdp=None,
                 population=None)
db.session.add(no_rep)
try:
    db.session.commit()
except Exception:
    db.session.rollback()
    
    
for i in range(len(gold_table)):
    row = gold_table.iloc[i]
    row_array = []
    for j in range(len(row)):
        row_array.append(row[j])
        if row.index[j] == 'Country':
            country = Country.query.filter_by(name=row[j]).first()
            if country is None:
                primary = no_rep_id
            else:
                primary = country.id
    row_array.append(primary)
    post_array = Gold(year=int(row_array[0]),  
                      city=row_array[1],
                      sport=row_array[2],
                      discipline=row_array[3], 
                      name=row_array[4], 
                      country=row_array[5], 
                      gender=row_array[6], 
                      event=row_array[7], 
                      season=row_array[8], 
                      country_id=row_array[9])
    db.session.add(post_array)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        

countries = Country.query.all()
for i in range(len(countries)):
    country = countries[i]
    num_golds = Gold.query.filter_by(country=country.name).count()
    if num_golds > 0:
        country = Country.query.get(i+1)
        country.medals = num_golds
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            

golds = Gold.query.filter_by()
for i in range(len(countries)):
    golds = Gold.query.filter_by()
    

sport_table = db.session.query(distinct(Gold.country), Gold.country_id).all()    
for i in range(len(sport_table)):
    country = sport_table[i][0]
    golds = Gold.query.filter_by(country=country).all()
    is_listed = Country.query.filter_by(name=country).first()
    if golds is None or is_listed is None:
        continue
    else:
        total = len(golds)
        counts = {}
        for gold in golds:
            counts[gold.sport] = 0
        for gold in golds:
            counts[gold.sport] += 1
        for key, value in counts.items():
            name = key
            count = value
            percent = '{0:.1f}'.format((value/total)*100)
            country_id = sport_table[i][1]
            post = Sport(name=name,  
                         count=count,
                         percent=percent,
                         country_id=country_id)
            db.session.add(post)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()

        
db.session.close()
