def test_is_clubs_list_reachable(client, mocker_loadClubs):
    assert client.get('/clubs-list')
