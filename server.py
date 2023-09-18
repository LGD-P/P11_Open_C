import json
from flask import Flask,render_template,request,redirect,flash,url_for
import os

def get_absolute_path(file):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return  os.path.join(base_dir, file)


def loadClubs():
    file_path = get_absolute_path('clubs.json')
    with open(file_path) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

def loadCompetitions():
    file_path = get_absolute_path('competitions.json')
    with open(file_path) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    error = "The address you entered does not match \
        no registered clubs. Please enter a valid address."
    club = [club for club in clubs if club['email'] == request.form['email']]
    if len(club) == 0:
        return (render_template('index.html', error=error), 400)

    return render_template('welcome.html', club=club[0],
                           competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))