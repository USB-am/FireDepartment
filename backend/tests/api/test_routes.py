import os
import unittest

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from . import BASE_URL, get_token
# from data_base import models


TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)


class TestLogin(unittest.TestCase):
	''' Tests for /login route '''

	def test_get_token(self):
		response = requests.post(
			os.path.join(BASE_URL, 'login'),
			json={
				'email': 'test',
				'password': 'test'
			}
		)

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.json().keys(), {'access_token'})


class TestGetEntryById(unittest.TestCase):
	''' Tests for /get_entry_by_id route '''

	def send_request(self, tablename: str) -> requests.Response:
		return requests.get(
			os.path.join(BASE_URL, f'model/{tablename}/1'),
			headers={'Authorization': self.token}
		)

	@classmethod
	def setUpClass(cls):
		cls.token = get_token()

		with Session(engine) as session:
			# test_short = models.Short(title='TestShort', into_new_line=False, explanation='TestShortExplanation')
			# session.add(test_short)
			
			session.commit()

	def test_tag_response(self):
		response = self.send_request('Tag')
		self.assertEqual(response.json().keys(), {'id', 'title'})

	def test_rank_response(self):
		response = self.send_request('Rank')
		self.assertEqual(response.json().keys(), {'id', 'title', 'priority'})

	def test_position_response(self):
		response = self.send_request('Position')
		self.assertEqual(response.json().keys(), {'id', 'title'})

	def test_emergency_response(self):
		response = self.send_request('Emergency')
		self.assertEqual(response.json().keys(), {'id', 'title', 'description', 'urgent'})

	# def test_short_response(self):
	# 	response = self.send_request('Short')
	# 	self.assertEqual(response.json().keys(), {'id', 'title', 'explanation', 'into_new_line'})

	def test_not_exists_tablename(self):
		response = self.send_request('sdlfnzlsjbfkjzdbflkjfbgkjb')
		self.assertEqual(response.status_code, 404)
