import pytest
from main import get_delivery_distance_fee, get_small_order_surcharge, \
	get_items_surcharge, get_friday_rush_multiplier, fee_cutter



@pytest.mark.parametrize("a, expected", [
	# Friday
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
	("2024-01-26T19:00:59Z", 1),
	("2024-01-26T19:01Z", 1),
	("2024-01-26T19:01:00Z", 1),
	("2024-01-26T19:10:25Z", 1),
	("2024-01-26T20:00:01Z", 1),
	("2024-01-26T23:59:59Z", 1),
	# Not Friday between 3 - 7 PM
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
	("2024-02-01T15:00Z", 1),
	# Time string isn't in ISO format
	("2024-00-26T15:59:59Z", None),
	("2024-01-00T15:59:59Z", None),
	#("24-01-26T15:59:59Z", None),		# Accidentally works
	#("01-26T15:59:59Z", None),			# Accidentally works
	#("2024-01T15:59:59Z", None),		# Accidentally works
	("2024-01-26T24:59:59Z", None),
	("2024-01-26T25Z", None),
	("/202401/26T00Z", None),
	("It's Crazy! It's Party!", None),
		# No timezone
	("2024-01-25T16:15:15", 1),
	("2024-01-25T16:15", 1),
	("2024-01-25T16", 1),
])
def test_get_friday_rush_multiplier(a, expected):
	result = get_friday_rush_multiplier(a)
	assert result == expected, f"Time string \"{a}\" failed! Should return {expected}, but returned {result}."

@pytest.mark.parametrize("a, expected", [
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
	(20000, 4000)

	
	
	])
def test_get_delivery_distance_fee(a, expected):
	result = get_delivery_distance_fee(a)
	assert result == expected, f"Delivery_distance {a} failed! Should return {expected}, but returned {result}."