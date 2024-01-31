import pytest
from main import get_delivery_distance_fee, get_small_order_surcharge, \
	get_items_surcharge, get_friday_rush_multiplier, fee_cutter


@pytest.mark.parametrize("input, expected", [
	("2024-01-26T00:00:00Z", 1),
	("2024-01-26T00:00Z", 1),
	("2024-01-26T00:00Z", 1),
	("2024-01-26T03:00Z", 1),
	("2024-01-26T03:00Z", 1),
	("2024-01-26T03:15Z", 1),
	("2024-01-26T04:15Z", 1),
	("2024-01-26T07:00Z", 1),
	("2024-01-26T07:00Z", 1),
	("2024-01-26T12:00Z", 1),
	("2024-01-26T14:00:59Z", 1),
	("2024-01-26T14:59:59Z", 1),
	("2024-01-26T14:59Z", 1),
	("2024-01-26T15:00:00Z", 1.2),
	("2024-01-26T15:00Z", 1.2),
	("2024-01-26T15Z", 1.2),
	("2024-01-26T15:00:01Z", 1.2),
	("2024-01-26T15:00:59Z", 1.2),
	("2024-01-26T15:59:59Z", 1.2),
	("2024-01-26T16:59:59Z", 1.2),
	("2024-01-26T17:01:01Z", 1.2),
	("2024-01-26T18:59:59Z", 1.2),
	("2024-01-26T19:00:00Z", 1.2),
	("2024-01-26T19:00Z", 1.2),
	("2024-01-26T19Z", 1.2),
	("2024-01-26T19:00:01Z", 1),
	("2024-01-26T19:01Z", 1),
	("2024-01-26T19:00:59Z", 1),
	("2024-01-26T19:01:00Z", 1),
	("2024-01-26T19:10:25Z", 1),
	("2024-01-26T20:00:01Z", 1),
	("2024-01-26T23:59:59Z", 1)
])
def test_get_friday_rush_multiplier_during_friday(input, expected):
	result = get_friday_rush_multiplier(input)
	assert result == expected, f"Time string \"{input}\" failed! Should return {expected}, but returned {result}."


@pytest.mark.parametrize("input, expected", [
	("2024-01-20T16:15:15Z", 1),
	("2024-01-21T16:15:15Z", 1),
	("2024-01-22T16:15:15Z", 1),
	("2024-01-23T16:15:15Z", 1),
	("2024-01-24T16:15:15Z", 1),
	("2024-01-25T16:15:15Z", 1),
	("2024-01-27T15:00:00Z", 1),
	("2024-01-28T15:00:00Z", 1),
	("2024-01-29T15Z", 1),
	("2024-01-30T15Z", 1),
	("2024-01-31T15:00Z", 1),
	("2024-02-01T15:00Z", 1)
])
def test_get_friday_rush_multiplier_not_friday(input, expected):
	result = get_friday_rush_multiplier(input)
	assert result == expected, f"Time string \"{input}\" failed! Should return {expected}, but returned {result}."


@pytest.mark.parametrize("input, expected", [
	("2024-01-25T16:15:15", 1),
	("2024-01-25T16:15", 1),
	("2024-01-25T16", 1),
])
def test_get_friday_rush_multiplier_no_timezone(input, expected):
	result = get_friday_rush_multiplier(input)
	assert result == expected, f"Time string \"{input}\" failed! Should return {expected}, but returned {result}."


@pytest.mark.parametrize("input, expected_exception", [
	("2024-00-26T15:59:59Z", ValueError),
	("2024-01-00T15:59:59Z", ValueError),
	("24-01-26T15:59:59Z", ValueError),
	("01-26T15:59:59Z", ValueError),
	("2024-01T15:59:59Z", ValueError),
	("2024-01-26T24:59:59Z", ValueError),
	("2024-01-26T25Z", ValueError),
	("/202401/26T00Z", ValueError),
	("2024-01-25T16:15:15z", ValueError),
	("2024-01-25T16:15z", ValueError),
	("2024-01-25T16z", ValueError),
	("2024-01-26T", ValueError),
	("It's Crazy! It's Party!", ValueError),
	(42, AttributeError)
	
])
def test_get_friday_rush_multiplier_invalid_format(input, expected_exception):
	with pytest.raises(expected_exception):
		get_friday_rush_multiplier(input)


@pytest.mark.parametrize("input, expected", [
	(0, 200),
	(1, 200),
	(499, 200),
	(500, 200),
	(501, 200),
	(999, 200),
	(1000, 200),
	(1001, 300),
	(1499, 300),
	(1500, 300),
	(1501, 400),
	(1999, 400),
	(2000, 400),
	(2001, 500),
	(2499, 500),
	(2500, 500),
	(2501, 600),
	(20000, 4000),
	(20000000, 4000000),
])
def test_get_delivery_distance_fee(input, expected):
	result = get_delivery_distance_fee(input)
	assert result == expected, f"get_delivery_distance_fee failed with value {input}! Should return {expected}, but returned {result}."


@pytest.mark.parametrize("input, expected_total", [
	(0, 1000),
	(1, 1000),
	(10, 1000),
	(99, 1000),
	(100, 1000),
	(101, 1000),
	(199, 1000),
	(300, 1000),
	(401, 1000),
	(450, 1000),
	(551, 1000),
	(999, 1000),
	(1000, 1000),
])
def test_get_small_order_surcharge_fee(input, expected_total):
	result = get_small_order_surcharge(input)
	assert result + input == expected_total, f"get_small_order_surcharge failed with value {input}! Should return {expected_total - input}, but returned {result}."



@pytest.mark.parametrize("input, expected", [
	(1000, 0),
	(1001, 0),
	(1002, 0),
	(1010, 0),
	(42000, 0),
	(825012, 0),
])
def test_get_small_order_surcharge_no_fee(input, expected):
	result = get_small_order_surcharge(input)
	assert result == expected, f"get_small_order_surcharge failed with value {input}! Should return 0, but returned {result}."


@pytest.mark.parametrize("input, expected", [
	(0, 0),
	(4, 0),
	(5, 50),
	(10, 300),
	(12, 400),
	(13, 570),
	(14, 620)
])
def test_get_items_surcharge(input, expected):
	result = get_items_surcharge(input)
	assert result == expected, f"get_items_surcharge failed with value {input}! Should return {expected}, but returned {result}."



@pytest.mark.parametrize("input, expected", [
	(200, 200),
	(500, 500),
	(1000, 1000),
	(1500, 1500),
	(1501, 1500),
	(2500, 1500),
	(42000, 1500),
	(2500500, 1500),
])
def test_fee_cutter_fee(input, expected):
	result = fee_cutter(input, 2500)
	assert result == expected, f"fee_cutter failed with fee of {input}! Should return {expected}, but returned {result}."


@pytest.mark.parametrize("input, expected", [
	(0, 1200),
	(500, 1200),
	(19999, 1200),
	(20000, 0),
	(40000, 0),
	(999999999999, 0),
])
def test_fee_cutter_cart_value(input, expected):
	result = fee_cutter(1200, input)
	assert result == expected, f"fee_cutter failed with fcart_value of {input}! Should return {expected}, but returned {result}."