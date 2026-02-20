import os

import requests


BASE_URL = 'http://127.0.0.1:8000/'


def get_token() -> str:
	response = requests.post(
		os.path.join(BASE_URL, 'login'),
		json={
			'email': 'test',
			'password': 'test'
	})

	if response.status_code != 201:
		raise requests.exceptions.HTTPError(f'[{response.status_code}] {response.json()}')

	return response.json()['access_token']
