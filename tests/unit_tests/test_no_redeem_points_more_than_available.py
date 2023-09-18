from bs4 import BeautifulSoup

def test_enought_points_to_purchase(client,mocker_loadClubs,mocker_loadCompetitions):
    valid_response = client.post('/purchasePlaces', data={"club": "Dead Lift","competition": "Summer Festival",
                                                          "places": '2'})
    assert valid_response.status_code == 200



def test_not_enought_points_to_purchase(client, mocker_loadClubs, mocker_loadCompetitions):
        response = client.post('/purchasePlaces', data={"club": "Dead Lift",
                                                        "competition": "Summer Festival",
                                                        "places": '50'})

        soup = BeautifulSoup(response.data, 'html.parser')
        error_messages = soup.find('li', {'id': 'error_message'})
        print(error_messages)

        assert error_messages.contents[0].strip() == "Choice not available please check your points"