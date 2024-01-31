from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from validators import validate_time


app = FastAPI(title="Delivery Fee Calculator")


class Request_Payload(BaseModel):
	cart_value: int = Field(strict = True, ge = 0)
	delivery_distance: int = Field(strict = True, ge = 0)
	number_of_items: int = Field(strict = True, ge = 1)
	time: str
	
	@field_validator("time")
	def time_validator(cls, value):
		return validate_time(value)


class Response_Payload(BaseModel):
	delivery_fee: int


@app.post("/delivery_fee/", response_model = Response_Payload)
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
	surcharge = (items - 4) * 50
	bulk_fee = 120
	if items > 12:
		return surcharge + bulk_fee
	return max(0, surcharge)

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



### ReadME

# testit selitettyinä
# -- error codes and assert values
#luettelo
# kirjastot ja versiot
# Keissit joita ei suojella:
# - ylimääräiset key value parit ja perustelut
# - sekaantunut järjestys


#### Heroku



# RuntimeError: The starlette.testclient module requires the httpx package to be installed.
#E   You can install this with:
#E       $ pip install httpx

