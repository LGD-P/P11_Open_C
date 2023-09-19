import datetime
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

def updateClubsPoints(club_name, new_value):
    file_path = get_absolute_path('clubs.json')
    with open(file_path, 'r+') as c:
        clubs = json.load(c)
        for club in clubs['clubs']:
            if club['name'] == club_name:
                club['points'] = new_value
        c.seek(0)
        json.dump(clubs, c, indent=4)
        c.truncate()

def loadCompetitions():
    file_path = get_absolute_path('competitions.json')
    with open(file_path) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def updateCompetitionPoints(competition_name, new_value):
    file_path = get_absolute_path('competitions.json')
    with open(file_path, 'r+') as c:
        competitions = json.load(c)
        for competition in competitions['competitions']:
            if competition['name'] == competition_name:
                competition['numberOfPlaces'] = new_value
        c.seek(0)
        json.dump(competitions, c, indent=4)
        c.truncate()

def checkCompetitionDate(competitions):
    booking_available = []
    current_date = datetime.datetime.now()
    for competition in competitions:
        competition_date = datetime.datetime.strptime(
            competition['date'], "%Y-%m-%d %H:%M:%S")
        if competition_date > current_date:
            booking_available.append(competition)
    return booking_available


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
available_competition = checkCompetitionDate(competitions)

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
                           competitions=competitions,available_competition=available_competition)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition,
                               available_competition=available_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions,
                               available_competition=available_competition)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    error_message = "Choice not available please check your points"
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = request.form['places']
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]

    if not placesRequired.isdigit():
        flash(error_message)
        return render_template('welcome.html', club=club,
                               competitions=competitions,available_competition=available_competition), 200

    placesRequired = int(request.form['places'])

    if 0 < placesRequired <= 12 and placesRequired <= int(club["points"]):
        club['points'] = str(int(club['points']) - placesRequired)
        competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
        updateClubsPoints(club['name'],club['points'])
        updateCompetitionPoints(competition['name'], competition['numberOfPlaces'])
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club,
                               competitions=competitions,available_competition=available_competition),200
    else:
        flash(error_message)
        return render_template('welcome.html', club=club,
                               competitions=competitions,available_competition=available_competition), 200




# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))