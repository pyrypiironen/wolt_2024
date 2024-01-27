from fastapi import FastAPI
from pydantic import BaseModel, conint



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
	
	# UTC
	if 1 == 1: 
		return 1.2
	else:
		return 1
	

###
def	fee_cutter(fee, cart_value):
	if cart_value >= 20000:
		fee = 0
	return min(fee, 1500)


#parametrize testaamiseen