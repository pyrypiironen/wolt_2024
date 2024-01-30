# Delivery Fee Calculator

This is my solution to [Wolt Summer 2024 Engineering Intership](https://github.com/woltapp/engineering-internship-2024).

I am applying for backend position using Python.

**Heroku

The Delivery Fee Calculator is an HTTP API (single POST endpoint), which calculates the delivery fee based on the information in
the request payload (JSON) and includes the calculated delivery fee in the response payload (JSON).

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

I used BaseModel, Field and field_validator from pydantic to build payloads, because this offered an opportunity to
keep code clean and not too bloated same time with good and partly automated error handling.

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

`Field(strict = True)` is for enforce strict type checking for the field it is applied to. Eg. string "5" or float 5.0
wouldn't raise an error without using this.

`ge = 0` and `ge = 1` are for minimum values for the int (ge = greater or equal).

`@field_validator("time")` validate the time from Request_Payload.
 - Validate that time is a string.
 - Validate that the string is on ISO format.
 - Validate that ISO format includes time part, not only date part
   - I did this by checking if the string includes T. If not, it cannot be on ISO format including time part.
   - Even though the Specification of the Preliminary Assignment doesn't specify that ISO format should be in some
specific form it would be impossible to check the Friday Rush without exact time so I decide to handle ISO format without time part as an invalid input.

<details>
<summary>Click here to see code.</summary>
	
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
My app using FastAPI Endpoint at the URL path `"/delivery_fee/"`, specifies Response Model, define the function for the actual endpoint handler, make the function call for `delivery_fee_calculator` and returns Response_Payload with calculated value.

<details>
<summary>Click here to see code.</summary>
	
```python
@app.post("/delivery_fee/", response_model = Response_Payload)
async def make_Response_Payload(Request_Payload: Request_Payload):
	fee = delivery_fee_calculator(Request_Payload)
	return Response_Payload(delivery_fee = fee)
```
</details>

### Delivery Fee Calculator

The main functionality of application has build in `delivery_fee_calculator`.

It takes in the Request_Payload and using values of the payload to calculate the correct delivery fee.

<details>
<summary>Click here to see code.</summary>
	
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



