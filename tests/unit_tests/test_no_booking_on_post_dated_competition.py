from  bs4 import BeautifulSoup


def test_is_competition_postdated(client,mocker_loadCompetitions,mocker_loadClubs):
    response = client.post('/showSummary', data={"email": "kate@strongirls.co.uk"})

    soup = BeautifulSoup(response.data, 'html.parser')

    if  soup.find('span', {'id': 'competition done'}):
        message = soup.find('span', {'id': 'competition done'})
        assert message.contents[0].strip() == "Compétition terminée"


def test_is_competition_available(client,mocker_loadCompetitions,mocker_loadClubs, mocker_checkCompetitionDate):
    response = client.post('/showSummary', data={"email": "kate@strongirls.co.uk"})
    test = mocker_checkCompetitionDate
    print(test)
    soup = BeautifulSoup(response.data, 'html.parser')
    print(soup)
    message = soup.find('a', {'id': 'competition available'})
    print( message)
    assert message.contents[0].strip() == "Book Places"