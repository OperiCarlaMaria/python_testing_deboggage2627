import json
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

## bug 2 points
def bookPlaces(club, competition, placesRequired): 
    club['points'] = int(club['points']) - placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    
## bug 3 points insuffisant et réservation allant au delà
def validatePurchase(club, competition, placesRequired):
    if placesRequired > int(club['points']):
        return "Not enough points to book that many places."
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


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

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