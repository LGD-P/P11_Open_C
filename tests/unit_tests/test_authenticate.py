from bs4 import BeautifulSoup

def test_index_page_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_showSummary_valid_response(client, mocker_loadClubs):
    valid_response = client.post('/showSummary',
                                 data={"email": "admin@ironfest.com"})
    assert valid_response.status_code == 200



def test_email_not_in_data_base_to_authenticate(client):
    bad_response = client.post('/showSummary',
                               data={"email": "jhn@deadlift.co"})

    assert bad_response.status_code == 400
    soup = BeautifulSoup(bad_response.data, 'html.parser')
    first_p =  soup.find("p", {"id": "error"})

    assert first_p.contents[0].strip() == "The address you entered does not match \
        no registered clubs. Please enter a valid address.".strip()