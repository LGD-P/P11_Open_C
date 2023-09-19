from  bs4 import BeautifulSoup


def test_is_competition_postdated(client,mocker_loadCompetitions,mocker_loadClubs):
    response = client.post('/showSummary', data={"email": "kate@strongirls.co.uk"})

    soup = BeautifulSoup(response.data, 'html.parser')

    if  soup.find('span', {'id': 'competition done'}):
        message = soup.find('span', {'id': 'competition done'})
        assert message.contents[0].strip() == "Compétition terminée"


def test_is_competition_available(client,mocker_loadCompetitions,mocker_loadClubs, mocker_checkCompetitionDate):
    response = client.post('/showSummary', data={"email": "kate@strongirls.co.uk"})
    soup = BeautifulSoup(response.data, 'html.parser')
    message = soup.find('a', {'id': 'competition available'})
    assert message.contents[0].strip() == "Book Places"


def test_is_user_trying_prohibited_booking(client,mocker_loadClubs,mocker_loadCompetitions):
    response = client.get("/book/Summer Festival/Strong girls")
    soup = BeautifulSoup(response.data, 'html.parser')
    print(soup)
    error_messages = soup.find('li', {'id': 'error_message'})
    assert error_messages.contents[0].strip() == "Something went wrong-please try again"


