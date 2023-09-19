import datetime

from pytest import fixture
from P11_Open_C.server import app



@fixture
def client():
    with app.test_client() as client:
        yield client

@fixture
def mocker_loadClubs(mocker):
    clubs =  [
        {
            "name": "Dead Lift", "email": "john@deadlift.co",
            "points": "11"
        },
        {
            "name": "Iron Fest","email": "admin@ironfest.com",
            "points": "6"
        },
        {
            "name": "Strong girls", "email": "kate@strongirls.co.uk",
            "points": "12"
        }
    ]
    mocker.patch('P11_Open_C.server.clubs', clubs)
    return clubs


@fixture
def mocker_loadCompetitions(mocker):
    competitions =  [
                {
                    "name": "Summer Festival", "date": "2023-08-27 10:30:00",
                    "numberOfPlaces": "11"
                },
                {
                    "name": "Heavy Fest", "date": "2024-10-22 14:00:00",
                    "numberOfPlaces": "25"
                }
            ]

    mocker.patch('P11_Open_C.server.competitions', competitions)
    return competitions



@fixture
def mocker_checkCompetitionDate(mocker, mocker_loadCompetitions):
    competitions = mocker_loadCompetitions
    booking_available = []
    current_date = datetime.datetime.now()
    for competition in competitions:
        competition_date = datetime.datetime.strptime(
            competition['date'], "%Y-%m-%d %H:%M:%S")
        if competition_date > current_date:
            booking_available.append(competition)

    mocker.patch('P11_Open_C.server.available_competition',booking_available)
    return booking_available
