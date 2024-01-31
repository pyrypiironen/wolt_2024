from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_invalid_cart_value():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": -1,
			"delivery_distance": 1500,
			"number_of_items": 5,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_invalid_delivery_distance():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": -1,
			"number_of_items": 5,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_empty_cart():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1500,
			"number_of_items": 0,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_invalid_time_string():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1500,
			"number_of_items": 5,
			"time":  "31st of January 12 PM"
		},
	)
	assert response.status_code != 200

def test_invalid_cart_value_format_str():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": "5",
			"delivery_distance": 1500,
			"number_of_items": 5,
			"time": "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_invalid_cart_value_format_float():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 5.0,
			"delivery_distance": 1500,
			"number_of_items": 5,
			"time": "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_invalid_delivery_distance_format():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": True,
			"number_of_items": 5,
			"time": "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200
	
def test_invalid_number_of_items_format():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1500,
			"number_of_items": 10.0,
			"time": "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200
	
def test_invalid_time_format():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1500,
			"number_of_items": 5,
			"time": 19.00
		},
	)
	assert response.status_code != 200

def test_ISO_format_without_time():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1500,
			"number_of_items": 5,
			"time": "2021-10-12"
		},
	)
	assert response.status_code != 200

def test_no_cart_value():
	response = client.post(
		"/delivery_fee/",
		json = {
			"delivery_distance": 1500,
			"number_of_items": 5,
			"time": "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_no_delivery_distance():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"number_of_items": 5,
			"time": "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_no_number_of_items():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1500,
			"time": "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code != 200

def test_no_time():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1500,
			"number_of_items": 4
		},
	)
	assert response.status_code != 200

def test_empty_payload():
	response = client.post(
		"/delivery_fee/",
		json = {
		},
	)
	assert response.status_code != 200
