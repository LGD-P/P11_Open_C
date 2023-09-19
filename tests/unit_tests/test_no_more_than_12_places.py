

def test_enought_points_to_purchase(client,mocker_loadClubs,mocker_loadCompetitions):
    valid_response = client.post('/purchasePlaces', data={"club": "Dead Lift","competition": "Summer Festival",
                                                          "places": '2'})
    assert valid_response.status_code == 200