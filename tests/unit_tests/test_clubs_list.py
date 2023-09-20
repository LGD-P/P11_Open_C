from bs4 import BeautifulSoup


def test_is_clubs_list_reachable(client, mocker_loadClubs):
    assert client.get('/clubs-list')


def test_is_clubs_list_displayed(client, mocker_loadClubs):
    response = client.get('/clubs-list')
    soup = BeautifulSoup(response.data, "html.parser")
    rows = soup.find_all('tr', class_='data')
    datas =  sorted(mocker_loadClubs, key=lambda x: int(x['points']), reverse=True)
    assert len(rows)  == len(mocker_loadClubs)
    for i, row in enumerate(rows):
        cells = row.find_all('td')
        assert cells[0].text.strip() == datas[i]['points']
        assert cells[1].text.strip() == datas[i]['name']
        assert cells[2].text.strip() == datas[i]['email']