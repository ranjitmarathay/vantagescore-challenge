import pytest
from database.database import get_db
from .conftest import client, test_db


def test_hello(client):
    response = client.get("/hello")
    print("printing response from hello", response)
    assert response.status_code == 200
    print("printing response from hello", response.json())
    assert response.json() == {"message": "Vantage Score Challenge"}

def test_get_properties(client):
    response = client.get("/property")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_one_property(client):
    response = client.get("/property/1")
    response_data = response.json()
    expected_data = {'id': 1, 'title': 'Test Property', 'address': '123 Test St', 'unit': 'A', 'property_value': 100000, 'year_built': 2022, 'bed': 2, 'bath': 1, 'sleeps': 4, 'sqft': 1000, 'lot_size': 1000, 'description': 'Test description', 'image_url': 'https://example.com/', 'url': 'https://example.com/', 'last_updated': '2024-04-26T11:50:56.115453', 'nightly_rate': 200.0, 'property_type': 'Duplex'}
    assert response.status_code == 200
    for key, value in response_data.items():
        if key != 'last_updated':
            assert value == expected_data[key]

def test_get_one_property_dne(client):
    response = client.get("/property/100")
    assert response.status_code == 404

def test_create_property(client):
    insert_data = {
        "title": "Airbnb",
        "address": "9107 Japonica Ct Austin Texas 78748",
        "unit": "A",
        "property_value": 586000,
        "year_built": "1987",
        "bed": 2,
        "bath": 2,
        "sleeps": 6,
        "sqft": 1200,
        "lot_size": 3500,
        "description": "Beautifully updated condo",
        "image_url": "https://example.com/",
        "url": "https://example.com/",
        "last_updated": "2024-04-26T04:54:17.673Z",
        "nightly_rate": 200,
        "property_type": "Duplex"
    }
    response = client.post("/property", json=insert_data)
    print(response.json())
    response_data = response.json()
    response_data['message'] = 'Property created'
    for k, v in response_data['property'].items():
        if k != 'last_updated':
            assert v == insert_data[k]
    assert response.status_code == 200

def test_update_property(client):
    update_data = {
        "nightly_rate": 300
    }
    response = client.put("/property/1", json=update_data)
    response_data = response.json()
    assert response_data['message'] == 'Property updated'
    assert response_data['property']['nightly_rate'] == 300
    assert response.status_code == 200

def test_update_property_dne(client):
    update_data = {
        "nightly_rate": 300
    }
    response = client.put("/property/100", json=update_data)
    assert response.status_code == 404

def test_delete_property(client):

    response = client.get("/property")
    before_delete_length = len(response.json())

    response = client.delete("/property/2")
    response_data = response.json()
    assert response_data['message'] == 'Property deleted'
    assert response.status_code == 200
    assert response_data['property_id'] == 2
    
    response = client.get("/property")
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()) == before_delete_length - 1