from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_valid():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1501,
			"number_of_items": 5,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert 0 <= delivery_fee <= 1500, f"Expected delivery fee is between 0 and 1500, got {delivery_fee}"

def test_zero_cart_value():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 0,
			"delivery_distance": 1501,
			"number_of_items": 5,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert 0 <= delivery_fee <= 1500, f"Expected delivery fee is between 0 and 1500, got {delivery_fee}"

def test_zero_delivery_distance():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 0,
			"number_of_items": 5,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert 0 <= delivery_fee <= 1500, f"Expected delivery fee is between 0 and 1500, got {delivery_fee}"

def test_one_item():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1501,
			"number_of_items": 1,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert 0 <= delivery_fee <= 1500, f"Expected delivery fee is between 0 and 1500, got {delivery_fee}"

def test_huge_cart_value():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 250000,
			"delivery_distance": 1501,
			"number_of_items": 9,
			"time":  "2024-01-25T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 0, f"Expected delivery fee is 1500, got {delivery_fee}"

def test_long_delivery_distance():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 65000,
			"number_of_items": 6,
			"time":  "2024-01-24T10:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 1500, f"Expected delivery fee is 1500, got {delivery_fee}"

def test_long_delivery_distance_with_friday_rush():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 65000,
			"number_of_items": 6,
			"time":  "2024-01-26T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 1500, f"Expected delivery fee is 1500, got {delivery_fee}"

def test_350_items():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1501,
			"number_of_items": 350,
			"time":  "2024-01-24T10:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 1500, f"Expected delivery fee is 1500, got {delivery_fee}"

def test_350_items_with_friday_rush():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1250,
			"delivery_distance": 1501,
			"number_of_items": 350,
			"time":  "2024-01-26T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 1500, f"Expected delivery fee is 1500, got {delivery_fee}"

def test_huge_values_with_friday_rush():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 250000,
			"delivery_distance": 65000,
			"number_of_items": 350,
			"time":  "2024-01-26T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 0, f"Expected delivery fee is 1500, got {delivery_fee}"

def test_effective_friday_rush():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1000,
			"delivery_distance": 200,
			"number_of_items": 2,
			"time":  "2024-01-26T16:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 240, f"Expected delivery fee is 240, got {delivery_fee}"

def test_same_without_rush():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1000,
			"delivery_distance": 200,
			"number_of_items": 2,
			"time":  "2024-01-24T10:14:00Z"
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 200, f"Expected delivery fee is 200, got {delivery_fee}"

def test_extra_key_value_pair():
	response = client.post(
		"/delivery_fee/",
		json = {
			"cart_value": 1000,
			"delivery_distance": 200,
			"number_of_items": 2,
			"time":  "2024-01-24T10:14:00Z",
			"customer_id": 42
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 200, f"Expected delivery fee is 200, got {delivery_fee}"

def test_extra_key_value_pair_mixed_order():
	response = client.post(
		"/delivery_fee/",
		json = {
			"number_of_items": 2,
			"time":  "2024-01-24T10:14:00Z",
			"customer_id": 42,
			"cart_value": 1000,
			"delivery_distance": 200
		},
	)
	assert response.status_code == 200
	response_data = response.json()
	delivery_fee = response_data.get('delivery_fee')
	assert delivery_fee == 200, f"Expected delivery fee is 200, got {delivery_fee}"
