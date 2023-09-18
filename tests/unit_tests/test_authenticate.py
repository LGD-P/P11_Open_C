

def test_index_page_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_showSummary_valid_response(client, mocker_loadClubs):
    valid_response = client.post('/showSummary',
                                 data={"email": "admin@ironfest.com"})
    assert valid_response.status_code == 200