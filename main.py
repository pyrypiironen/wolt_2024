from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from datetime import datetime


app = FastAPI(title="Delivery Fee Calculator")


class Request_Payload(BaseModel):
	cart_value: int
	delivery_distance: int
	number_of_items: int
	time: str

	@field_validator("cart_value")
	def validate_cart_value(cls, cart_value):
		if not isinstance(cart_value, int):
			raise ValueError("Error: cart_value must be an integer.")
		if cart_value < 0:
			raise ValueError("Error: cart_value cannot be negative.")
		return cart_value
	
	@field_validator("delivery_distance")
	def validate_delivery_distance(cls, delivery_distance):
		if not isinstance(delivery_distance, int):
			raise ValueError("Error: delivery_distance must be an integer.")
		if delivery_distance < 0:
			raise ValueError("Error: delivery_distance cannot be negative.")
		return delivery_distance
	
	@field_validator("number_of_items")
	def validate_number_of_items(cls, number_of_items):
		if not isinstance(number_of_items, int):
			raise ValueError("Error: number_of_items must be an positive integer.")
		if number_of_items < 0:
			raise ValueError("Error: number_of_items must be an positive integer.")
		return number_of_items
	
	@field_validator("time")
	def validate_time(cls, time):
		if not isinstance(time, str):
			raise ValueError("Error: time must be a string.")
		try:
			time = time.replace("Z", "+00:00")
			datetime.fromisoformat(time)
		except ValueError:
			raise ValueError("Error: time string must be in ISO format.")
		return time


class Response_Payload(BaseModel):
	delivery_fee: int


@app.post("/delivery_fee/", response_model=Response_Payload)
async def make_Response_Payload(Request_Payload: Request_Payload):
	fee = delivery_fee_calculator(Request_Payload)
	return Response_Payload(delivery_fee = fee)


def delivery_fee_calculator(Request_Payload):
	fee = get_delivery_distance_fee(Request_Payload.delivery_distance)
	fee += get_small_order_surcharge(Request_Payload.cart_value)
	fee += get_items_surcharge(Request_Payload.number_of_items)
	fee *= get_friday_rush_multiplier(Request_Payload.time)
	fee = fee_cutter(fee, Request_Payload.cart_value)
	return int(fee)


def get_delivery_distance_fee(delivery_distance):
	fee = 0
	while delivery_distance > 0:
		fee += 100
		delivery_distance -= 500
	return max(200, fee)


def get_small_order_surcharge(cart_value):
	return max(1000 - cart_value, 0)


def get_items_surcharge(items):
	fee = 0
	bulk_fee = 0
	if items > 4:
		fee = (items - 4) * 50
		if items > 12:
			bulk_fee = 120
	return fee + bulk_fee


def get_friday_rush_multiplier(time):
		dt_object = create_datetime_object(time)
		weekday = dt_object.strftime("%A")
		start_time = dt_object.replace(hour = 15, minute = 0, second = 0, microsecond = 0)
		end_time = dt_object.replace(hour = 19, minute = 0, second = 0, microsecond = 0)
		if weekday == "Friday" and start_time <= dt_object <= end_time:
				return 1.2
		return 1	


def create_datetime_object(time):
	time = time.replace("Z", "+00:00")
	dt_object = datetime.fromisoformat(time)
	return dt_object


def	fee_cutter(fee, cart_value):
	if cart_value >= 20000:
		fee = 0
	return min(fee, 1500)







# uvicorn main:app --reload

# 2024-01-15T13:00:00Z



# Testaa Request Payloadilla
## Tarkista testit ja Specification, ettei ajatusvirheitä
### ReadME
#### Heroku



# RuntimeError: The starlette.testclient module requires the httpx package to be installed.
#E   You can install this with:
#E       $ pip install httpx

