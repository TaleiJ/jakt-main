from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Event
import json
import sqlite3

bp = Blueprint('main', __name__)

def getGenreList(): #Retrieve/displaying all available crypto assets/coins
    eventGENRE = [] 
    with open('GenreList.json') as json_file: # open the JSON file 
        genrelist = json.load(json_file) # load the data into an array  
        #display each element in the array 
        for g in genrelist['genrelist']:
            eventGENRE.append(g["name"])
        eventGENRE.sort()
        return eventGENRE 

@bp.route('/')
def index():
    
    event = Event.query.all()
    return render_template('index.html', event=event)

@bp.route('/search')
def search():
    if request.args.get('eventsearch', False):
        print(request.args['eventsearch'])
        evensearch = '%' + request.args['eventsearch'] + '%'
        eventsearch = Event.query.filter(Event.name.like(evensearch)).all()
        return render_template('index.html', event=eventsearch)

    else:
        return redirect(url_for('main.index'))

@bp.route('/genre')
def genre():
    if request.args.get('genresearch', False):
        print(request.args['genresearch'])
        gensearch = '%' + request.args['genresearch'] + '%'
        genresearch = Event.query.filter(Event.genre.like(gensearch)).all()
        return render_template('index.html', event=genresearch)
    else:
        return redirect(url_for('main.index'))

@bp.route('/venue')
def venue():
    if request.args.get('venuesearch', False):
        print(request.args['venuesearch'])
        vensearch = '%' + request.args['venuesearch'] + '%'
        venuesearch = Event.query.filter(Event.venue.like(vensearch)).all()
        return render_template('index.html', event=venuesearch)
    else:
        return redirect(url_for('main.index'))

@bp.route('/status')
def status():
    if request.args.get('statussearch', False):
        print(request.args['statussearch'])
        stasearch = '%' + request.args['statussearch'] + '%'
        statussearch = Event.query.filter(Event.status.like(stasearch)).all()
        return render_template('index.html', event=statussearch)
        
    else:
        return redirect(url_for('main.index'))