from bs4 import BeautifulSoup


def test_login_and_book_until_not_enough_points(client, mocker_loadClubs,mocker_loadCompetitions):
    response = client.get('/')
    assert response.status_code == 200

    valid_response = client.post('/showSummary',
                                 data={"email": "admin@ironfest.com"})
    assert valid_response.status_code == 200

    competitions = mocker_loadCompetitions
    competition = [c for c in competitions if c['name'] == "Heavy Fest"][0]
    initial_points = competition["numberOfPlaces"]
    assert initial_points == "25"

    clubs = mocker_loadClubs
    club = [club for club in clubs if club['name'] == 'Iron Fest'][0]
    initial_points = club["points"]
    assert initial_points == "6"

    expected_message = "Great-booking complete!".strip()

    book = client.post('/purchasePlaces', data={"club": "Iron Fest",
                                                    "competition": "Heavy Fest",
                                                    "places": "3"})

    updated_points = competition["numberOfPlaces"]
    assert updated_points == "22"

    updated_points = club["points"]
    assert updated_points == "3"

    soup = BeautifulSoup(book.data, 'html.parser')
    message = soup.find('li', {'id': 'error_message'})
    assert message.contents[0].strip() == expected_message

    error_message = "Choice not available please check your points".strip()
    second_book = client.post('/purchasePlaces', data={"club": "Iron Fest",
                                                "competition": "Heavy Fest",
                                                "places": "4"})

    soup = BeautifulSoup(second_book.data, 'html.parser')
    message = soup.find('li', {'id': 'error_message'})
    assert message.contents[0].strip() == error_message

    assert updated_points == "3"

def test_wrong_login_then_wrong_purchase_logout(client, mocker_loadClubs,mocker_loadCompetitions):
    response = client.get('/')
    assert response.status_code == 200

    bad_response = client.post('/showSummary',
                                 data={"email": "admn@ironfest.com"})
    assert bad_response.status_code == 400

    soup = BeautifulSoup(bad_response.data, 'html.parser')
    first_p =  soup.find("p", {"id": "error"})
    assert first_p.contents[0].strip() == "The address you entered does not match \
        no registered clubs. Please enter a valid address.".strip()

    valid_response = client.post('/showSummary',
                                 data={"email": "admin@ironfest.com"})
    assert valid_response.status_code == 200

    response = client.get("/book/Summer Festival/Iron Fest")
    soup = BeautifulSoup(response.data, 'html.parser')
    error_messages = soup.find('li', {'id': 'error_message'})
    assert error_messages.contents[0].strip() == "Something went wrong-please try again"

    response = client.get("/logout", follow_redirects=True)
    assert response

    soup = BeautifulSoup(response.data, 'html.parser')
    logout_message = soup.find("li", {"id": "logout done"})
    assert logout_message.text == "Logout success"



