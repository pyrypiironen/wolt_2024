# Delivery Fee Calculator

This is my solution to [Wolt Summer 2024 Engineering Internship](https://github.com/woltapp/engineering-internship-2024).

I am applying for a backend position using Python.

The Delivery Fee Calculator is an HTTP API (single POST endpoint), which calculates the delivery fee based on the information in the request payload (JSON) and includes the calculated delivery fee in the response payload (JSON).

## Usage

The Application starts running by `uvicorn main:app`

When the application is running you can send a POST request to `http://127.0.0.1:8000/delivery_fee/`

Press `CTRL + C` to stop running.

## Usage, option 2

**heroku

## Testing

### Unit tests

Usage: 

## My app

### Libraries and classes

I chose to use fastapi, pydantic and datetime libraries to build my application.

<details>
<summary>Click here to see all libraries and classes.</summary>
	
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from validators import validate_time
```
</details>

### Payloads and error handling

I used BaseModel, Field, and field_validator from pydantic to build payloads, because this offered an opportunity to
keep code clean and not too bloated at the same time with good and partly automated error handling.

<details>
<summary>Click here to see payloads.</summary>
	
```python
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
```
</details>

`Field(strict = True)` is for enforcing strict type checking for the field it is applied to. Eg. string "5" or float 5.0
wouldn't raise an error without using this.

`ge = 0` and `ge = 1` are for minimum values for the int (ge = greater or equal).

`@field_validator("time")` validate the time from Request_Payload.
 - Validate that time is a string.
 - Validate that the string is in ISO format.
 - Validate that ISO format includes the time part, not only the date part
   - I did this by checking if the string includes T. If not, it cannot be in ISO format including the time part.
   - Even though the Specification of the Preliminary Assignment doesn't specify that ISO format should be in some specific form it would only be possible to check the Friday Rush with the exact time so I decided to handle ISO format without the time part as an invalid input.

<details>
<summary>Click here to see the code.</summary>
	
```python
	@field_validator("time")
	def time_validator(cls, value):
		return validate_time(value)

# validators.py
def validate_time(time: str) -> str:
	if not isinstance(time, str):
		raise ValueError("Time isn't a string.")
	try:
		time = time.replace("Z", "+00:00")
		datetime.fromisoformat(time)
	except ValueError:
		raise ValueError("Time isn't in ISO format.")
	if 'T' not in time:
		raise ValueError("ISO format doesn't include time (T).")
	return time
```
</details>

### The Application

```python
app = FastAPI(title="Delivery Fee Calculator")
```
My app using FastAPI Endpoint at the URL path `"/delivery_fee/"`, specifies the Response Model, defines the function for the actual endpoint handler, makes the function call for `delivery_fee_calculator`, and returns Response_Payload with calculated value.

<details>
<summary>Click here to see the code.</summary>
	
```python
@app.post("/delivery_fee/", response_model = Response_Payload)
async def make_Response_Payload(Request_Payload: Request_Payload):
	fee = delivery_fee_calculator(Request_Payload)
	return Response_Payload(delivery_fee = fee)
```
</details>

### delivery_fee_calculator

The main functionality of the application is built in `delivery_fee_calculator`.

It takes in the Request_Payload and uses the values of the payload to calculate the correct delivery fee.

<details>
<summary>Click here to see the code.</summary>
	
```python
def delivery_fee_calculator(Request_Payload):
	fee = get_delivery_distance_fee(Request_Payload.delivery_distance)
	fee += get_small_order_surcharge(Request_Payload.cart_value)
	fee += get_items_surcharge(Request_Payload.number_of_items)
	fee *= get_friday_rush_multiplier(Request_Payload.time)
	fee = fee_cutter(fee, Request_Payload.cart_value)
	return int(fee)
```
</details>

### get_delivery_distance

`get_delivery_distance` counts the base fee of the order based on the delivery distance.
 - A delivery fee for the first 1000 meters (=1km) is 2€.
 - If the delivery distance is longer than that, 1€ is added for every additional 500 meters.
 
&rArr; The function adds 100 cents to the fee and reduces 500 meters from delivery_distance while delicery_distance is equal to or smaller than zero. In the end, it returns 200 or fee if the fee is more than 200.

<details>
<summary>Click here to see the code.</summary>
	
```python
def get_delivery_distance_fee(delivery_distance):
	fee = 0
	while delivery_distance > 0:
		fee += 100
		delivery_distance -= 500
	return max(200, fee)
```
</details>

### get_items_surcharge

`get_items_surcharge` count the additional surcharge based on the amount of items.
 - If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item.
 - An extra "bulk" fee applies for more than 12 items of 1,20€.

<details>
<summary>Click here to see the code.</summary>
	
```python
def get_items_surcharge(items):
	surcharge = (items - 4) * 50
	bulk_fee = 120
	if items > 12:
		return surcharge + bulk_fee
	return max(0, surcharge)
```
</details>

### get_friday_rush_multiplier

Add text

<details>
<summary>Click here to see the code.</summary>
	
```python
def get_friday_rush_multiplier(time):
		dt_object = create_datetime_object(time)
		weekday = dt_object.strftime("%A")
		start_time = dt_object.replace(hour = 15, minute = 0, second = 0, microsecond = 0)
		end_time = dt_object.replace(hour = 19, minute = 0, second = 0, microsecond = 0)
		if weekday == "Friday" and start_time <= dt_object <= end_time:
				return 1.2
		return 1
```
</details>
