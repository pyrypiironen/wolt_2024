from datetime import datetime	


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

