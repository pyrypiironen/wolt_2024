from fastapi import FastAPI
from pydantic import BaseModel, conint
from datetime import date, datetime, time
from zoneinfo import ZoneInfo
import pytz




app = FastAPI(title="Delivery Fee Calculator")

class Payload(BaseModel):
	cart_value: conint(ge=0)
	delivery_distance: conint(ge=0)
	number_of_items: conint(ge=0)
	time: str

class Response(BaseModel):
	delivery_fee: int


# Post endpoint
@app.post("/delivery_fee/", response_model=Response)
async def make_response(payload: Payload):
	fee = delivery_fee_calculator(payload)
	return Response(delivery_fee=fee)



def delivery_fee_calculator(payload):

	fee = 0
	fee += get_small_order_surcharge(payload.cart_value)
	fee += get_delivery_distance_fee(payload.delivery_distance)
	fee += get_items_surcharge(payload.number_of_items)
	fee *= get_friday_rush_multiplier(payload.time)
	fee = fee_cutter(fee, payload.cart_value)



	return int(fee)


###
def get_small_order_surcharge(cart_value):
	return max(1000 - cart_value, 0)


###
def get_delivery_distance_fee(distance):
	fee = 200
	distance -= 1000


	return fee


###
def get_items_surcharge(number_of_items):

	#remember bulk fee
	return 101


###
def get_friday_rush_multiplier(time):
	time_object = datetime.fromisoformat(time)
	start_rush = time_object.replace(hour = 15, minute = 0, second = 0)
	end_rush = time_object.replace(hour = 19, minute = 0, second = 0)
	utc_time_object = time_object.astimezone(ZoneInfo("UTC"))					## Check usage and del /// Only utc
	weekday = time_object.strftime("%A")										## Weekday
	
	
	## ## ## Testing
	print("--------------------------------------------------------------")
	print("time_object")
	print(time_object)
	print()
	print("utc_time_object --- we are not using this now")
	print(utc_time_object)
	print()
	print(start_rush)
	print()
	print(weekday)
	print()
	if weekday == "Friday":
		print("It really is a Friday")
	else:
		print("Today is " + weekday)
	
	print()
	weekdayAsNum = time_object.weekday()
	print("Weekday as number is " + str(weekdayAsNum))
	print("--------------------------------------------------------------")


	## ## ##
	if weekday == "Friday":
		if start_rush <= time_object <= end_rush:
			print("It is Friday rush!")
			print("get_friday_rush returned 1.2")
			print("--------------------------------------------------------------")
			return 1.2
		else:
			print("It is Friday, but not between 3 PM and 7 PM!")
			print("get_friday_rush returned 1")
			print("--------------------------------------------------------------")
			return 1
			
	else:
		print("It is not Friday!")
		print("get_friday_rush returned 1")
		print("--------------------------------------------------------------")
		return 1

###
def	fee_cutter(fee, cart_value):
	if cart_value >= 20000:
		fee = 0
	return min(fee, 1500)


#parametrize testaamiseen

# uvicorn main:app --reload

# 2024-01-15T13:00:00Z