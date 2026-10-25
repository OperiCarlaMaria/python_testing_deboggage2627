import json
from datetime import datetime ##ajout d'import pour les dates
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    # BUG n°9 : les points étaient des chaînes ("13"), on les convertit
    # en entiers dès le chargement
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
    for club in listOfClubs:
        club['points'] = int(club['points'])
    return listOfClubs


def loadCompetitions():
    # BUG n°9 : même correction pour le nombre de places
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
    for competition in listOfCompetitions:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
    return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

## bug 1 emails
def getClubByEmail(email): 
    return next((club for club in clubs if club['email'] == email), None)

## "bug" 7 eviter les erreurs du genre entré des chiffre négatifs etc...
def getClubByName(name):
    return next((club for club in clubs if club['name'] == name), None)


def getCompetitionByName(name):
    return next((c for c in competitions if c['name'] == name), None)

def getClubsPoints():
    # BUG n°11 : données du tableau public des points
    # On ne garde que le nom et les points (jamais l'email), triés par nom
    # pour ne favoriser aucun club
    return sorted(
        [{'name': c['name'], 'points': int(c['points'])} for c in clubs],
        key=lambda entry: entry['name'],
    )


def parsePlaces(raw):
    try:
        places = int(raw)
    except (TypeError, ValueError):
        return None
    return places if places >= 1 else None

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

## bug 6 date compétition/"bug" 7
@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = getClubByName(club)
    if foundClub is None:
        flash("Something went wrong-please try again")
        return render_template('index.html'), 404
    foundCompetition = getCompetitionByName(competition)
    if foundCompetition is None:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions), 404
    if isCompetitionPast(foundCompetition):
        flash("This competition is already over.")
        return render_template('welcome.html', club=foundClub, competitions=competitions)
    return render_template('booking.html', club=foundClub, competition=foundCompetition)

## changement de route bug 2 points et bug 3/ "bug" 7
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    club = getClubByName(request.form.get('club', ''))
    if club is None:
        flash("Something went wrong-please try again")
        return render_template('index.html'), 404
    competition = getCompetitionByName(request.form.get('competition', ''))
    if competition is None:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions), 404
    placesRequired = parsePlaces(request.form.get('places'))
    if placesRequired is None:
        flash("Please enter a valid number of places (1 or more).")
        return render_template('welcome.html', club=club, competitions=competitions)
    error = validatePurchase(club, competition, placesRequired)
    if error:
        flash(error)
        return render_template('welcome.html', club=club, competitions=competitions)
    bookPlaces(club, competition, placesRequired)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsBoard')
def pointsBoard():
    # BUG n°11 : page publique en lecture seule (GET uniquement),
    # accessible sans connexion
    return render_template(
        'points_board.html', clubs_points=getClubsPoints()
    )


@app.route('/logout')
def logout():
    return redirect(url_for('index'))