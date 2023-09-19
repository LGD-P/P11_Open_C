from  bs4 import BeautifulSoup


def test_is_competition_postdated(client,mocker_loadCompetitions,mocker_loadClubs):
    response = client.post('/showSummary', data={"email": "kate@strongirls.co.uk"})

    soup = BeautifulSoup(response.data, 'html.parser')

    if  soup.find('span', {'id': 'competition done'}):
        message = soup.find('span', {'id': 'competition done'})
        assert message.contents[0].strip() == "Compétition terminée"