# Delivery Fee Calculator

This is my solution to [Wolt Summer 2024 Engineering Internship](https://github.com/woltapp/engineering-internship-2024).

I am applying for a backend position using Python.

The Delivery Fee Calculator is an HTTP API (single POST endpoint), which calculates the delivery fee based on the
information in the request payload (JSON) and includes the calculated delivery fee in the response payload (JSON).

### Table of Contents

1. [Usage](#usage)
2. [Testing](#testing)
3. [My App](#my-app)

## Usage

Create an virtual environment by `python3 -m venv env`

Activate the virtual environment by `source env/bin/activate`

Use the command `pip install -r requirements.txt` to install specific packages and avoid version mismatch.

Make sure that you have Python version 3.11.1 or newer. The application may also work with older Python versions, but is tested by 3.11.1.

The Application starts running on your local machine by `uvicorn main:app`

When the application is running you can send a POST request to `http://127.0.0.1:8000/delivery_fee/`

Check [Payloads and error handling](#payloads-and-error-handling) for more information about the Request Payload.

Press `CTRL + C` to stop running.

Deactivate the virtual environment by `deactivate`

## Testing

### Unit Tests

Unit tests test every function used by `delivery_fee_calculator`. The test cases are chosen for testing edge cases and the behavior of code in points on thresholds. Unit tests don't test with invalid values. That part is covered by the next part
of testing.

Run the unit tests by `pytest test_unit_tests.py`

### Testing Request_Payload

Tests are split into two files; one for valid cases and one for error cases. The tests are planned to cover as much of the
undesirable use as possible and focus on the cases that wouldn't be tested by unit tests.

The error tests check that the response status code is not equal to 200 as well as the valid tests check that it is 200.
The valid tests also check that the delivery fee is in the range of 0 to 1500 or equal to 1500 or equal to 0. The best option is chosen for
every test particularly. This is accurate enough after a wide range of unit tests. Unit tests are for making sure that
the operating logic of the application works.

Run the tests by `pytest test_payload_valids.py test_payload_errors.py`

Run all tests at the same time by `pytest test_payload_valids.py test_payload_errors.py test_unit_tests.py`

<details>
<summary>Click here to see a list of valid tests.</summary>
	
![valid](https://github.com/pyrypiironen/wolt_2024/assets/93189576/35e905ac-c18b-4c1f-bee1-6a7dfa47aaaf)


</details>

<details>
<summary>Click here to see a list of error tests.</summary>
	
![error](https://github.com/pyrypiironen/wolt_2024/assets/93189576/412f83a9-038f-4c5e-8d8e-c7bf05136ff4)

</details>

## My App

### Libraries and classes

I chose to use fastapi, pydantic and datetime libraries to build my application.

<details>
<summary>Click here to see all libraries and classes.</summary>
	
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from validators import validate_time	#my own implement
```
</details>

### Payloads and Error Handling

I used BaseModel, Field, and field_validator from pydantic to build payloads, because this offered an opportunity to
keep code clean and not too bloated at the same time with good and partly automated error handling.

I haven't added custom error messages because pydantic's error messaging provides detailed and structured information about
each validation failure.

<details>
<summary>Click here to see payloads in my code.</summary>
	
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

I used `@field_validator("time")` to validate the time from Request_Payload.
 - Validate that time is a string.
 - Validate that the string is in ISO format.
 - Validate that ISO format includes the time part, not only the date part
   - I did this by checking if the string includes 'T'. If not, it cannot be in ISO format including the time part.
   - Even though the Specification of the Preliminary Assignment doesn't specify that ISO format should be in some specific
   form it would only be possible to check the Friday Rush with the exact time so I decided to handle ISO format without the
   time part as an invalid input.

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

#### Example of Request_Payload:
```python
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```
#### Note!

I decided to allow the extra key-value pairs in Request Payloads as well as a changed order.
This would give the opportunity eg. to add parameters to use the calculator or to add some metadata to JSON in the future and
wouldn't cause any misbehavior when using the application. It also would be justifiable to treat these cases as errors.

### The Application

```python
app = FastAPI(title="Delivery Fee Calculator")
```
My app using FastAPI Endpoint at the URL path `"/delivery_fee/"`, specifies the Response Model, defines the function for
the actual endpoint handler, makes the function call for `delivery_fee_calculator`, and returns Response_Payload with the calculated value.

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

There is no error handling inside this function. The error handling has been implemented earlier.

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
 
&rArr; The function adds 100 cents to the fee and reduces 500 meters from delivery_distance while delicery_distance is equal to
or smaller than zero. In the end, it returns 200 or fee if the fee is more than 200.

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

`get_friday_rush` creates the datetime object, defines the weekday, and then checks if the delivery time is on Friday between 3 and 7 PM (including
starting and ending points). If it is, the function returns a multiplier 1.2. Else it returns 1.
 - During the Friday rush, 3 - 7 PM, the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x.

The function doesn't cover other timezones as an input or check them in case of error. It just assumes that the input is in UTC as told.


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

### create_datetime_object

The "Z" in ISO format indicates UTC timezone, but as part of the string may cause an error when using `datetime.fromisoformat(time)`. To avoid errors in all cases, I replaced "Z" with "+00:00" which also indicates UTC timezone. After that, the function just creates the datetime object and returns it.

<details>
<summary>Click here to see the code.</summary>

```python
def create_datetime_object(time):
	time = time.replace("Z", "+00:00")
	dt_object = datetime.fromisoformat(time)
	return dt_object
```
</details>

### fee_cutter

`fee_cutter` cut the fee to a maximum of 1500 cents. If the cart_value is equal to or more than 200 euros (20 000 cents) the fee is 0.
 - The delivery fee can never be more than 15€, including possible surcharges.
 - The delivery is free (0€) when the cart value is equal to or more than 200€.

<details>
<summary>Click here to see the code.</summary>
	
```python
def	fee_cutter(fee, cart_value):
	if cart_value >= 20000:
		fee = 0
	return min(fee, 1500)
```
</details>
