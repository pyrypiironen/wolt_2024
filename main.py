from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from dateutil import parser
from datetime import datetime

#del
from typing import Union
import pytz




app = FastAPI(title="Delivery Fee Calculator")

class Request_Payload(BaseModel):
	cart_value: conint(ge=0)
	delivery_distance: conint(ge=0)
	number_of_items: conint(ge=0)
	time: str

class Response_Payload(BaseModel):
	delivery_fee: int




@app.post("/delivery_fee/", response_model=Response_Payload)
async def make_Response_Payload(Request_Payload: Request_Payload):
	fee = delivery_fee_calculator(Request_Payload)
	if fee == None:
		raise HTTPException(status_code = 400, detail = "Error: Time string isn't valid.")
	return Response_Payload(delivery_fee = fee)



def delivery_fee_calculator(Request_Payload):
	rush_multiplier = get_friday_rush_multiplier(Request_Payload.time)
	if rush_multiplier == None:
		return None
	# Change this to convert_time_str_to_object
	# --> Use more sopiscated functions
	fee = get_delivery_distance_fee(Request_Payload.delivery_distance)
	fee += get_small_order_surcharge(Request_Payload.cart_value)
	fee += get_items_surcharge(Request_Payload.number_of_items)
	fee *= rush_multiplier
	fee = fee_cutter(fee, Request_Payload.cart_value)


	return int(fee)





###
def get_delivery_distance_fee(delivery_distance):
	fee = 0
	while delivery_distance > 0:
		fee += 100
		delivery_distance -= 500
	return max(200, fee)




###
def get_small_order_surcharge(cart_value):
	return max(1000 - cart_value, 0)




###
def get_items_surcharge(items):
	fee = 0
	bulk_fee = 0
	if items > 4:
		fee = (items - 4) * 50
		if items > 12:
			bulk_fee = 120
	return fee + bulk_fee

###
def get_friday_rush_multiplier(time):
	try:
		time = time.replace("Z", "+00:00")
		time = time.replace("z", "+00:00") # not necessary
		dt_object = datetime.fromisoformat(time)
		start_rush = dt_object.replace(hour = 15, minute = 0, second = 0)
		end_rush = dt_object.replace(hour = 19, minute = 0, second = 0)
		weekday = dt_object.strftime("%A")
		if weekday == "Friday" and start_rush <= dt_object <= end_rush:
				return 1.2
		return 1
	except ValueError:
		return None
	


###
def	fee_cutter(fee, cart_value):
	if cart_value >= 20000:
		fee = 0
	return min(fee, 1500)



# uvicorn main:app --reload

# 2024-01-15T13:00:00Z



# Testaa Request Payloadilla
## Tarkista testit ja Specification, ettei ajatusvirheitä
### ReadME





