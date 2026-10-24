import json
from datetime import datetime ##ajout d'import pour les dates
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

## bug 1 emails
def getClubByEmail(email): 
    return next((club for club in clubs if club['email'] == email), None)

##bug 6 date compétition 
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def isCompetitionPast(competition):
    date = competition.get('date')
    if not date:
        return False
    return datetime.strptime(date, DATE_FORMAT) < datetime.now()


app.jinja_env.globals['is_past'] = isCompetitionPast

## bug 4 limite de réservation 
MAX_PLACES_PER_COMPETITION = 12


def getPlacesBooked(club, competition):
    return competition.get('booked', {}).get(club['name'], 0)

## bug 2 points/ bug 4
def bookPlaces(club, competition, placesRequired):
    club['points'] = int(club['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    booked = competition.setdefault('booked', {})
    booked[club['name']] = booked.get(club['name'], 0) + placesRequired
    
## bug 3 points insuffisant et réservation allant au delà/ bug 4/ bug 5/ bug 6
def validatePurchase(club, competition, placesRequired):
    available = int(competition['numberOfPlaces'])
    if isCompetitionPast(competition):
        return "This competition is already over."
    if available <= 0:
        return "This competition is full."
    if placesRequired > available:
        return "Not enough places available in this competition."
    if placesRequired > int(club['points']):
        return "Not enough points to book that many places."
    if getPlacesBooked(club, competition) + placesRequired > MAX_PLACES_PER_COMPETITION:
        return "You cannot book more than 12 places per competition."
    return None

@app.route('/')
def index():
    return render_template('index.html')

## changement de route bug 1 emails
@app.route('/showSummary', methods=['POST']) 
def showSummary():
    club = getClubByEmail(request.form.get('email', ''))
    if club is None:
        flash("Sorry, that email was not found.")
        return render_template('index.html')
    return render_template('welcome.html', club=club, competitions=competitions)

## bug 6 date compétition
@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        if isCompetitionPast(foundCompetition):
            flash("This competition is already over.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

## changement de route bug 2 points et bug 3
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    error = validatePurchase(club, competition, placesRequired)
    if error:
        flash(error)
        return render_template('welcome.html', club=club, competitions=competitions)
    bookPlaces(club, competition, placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))