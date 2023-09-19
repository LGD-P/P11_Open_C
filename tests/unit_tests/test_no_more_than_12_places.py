from bs4 import BeautifulSoup


def test_less_or_equal_12_places_to_purchase(client,mocker_loadClubs,mocker_loadCompetitions):
    valid_max_purchase = 12

    expected_message = "Great-booking complete!".strip()

    response = client.post('/purchasePlaces', data={"club": "Strong girls",
                                                    "competition": "Heavy Fest",
                                                    "places": str(
                                                        valid_max_purchase)})

    soup = BeautifulSoup(response.data, 'html.parser')
    message = soup.find('li', {'id': 'error_message'})
    assert message.contents[0].strip() == expected_message