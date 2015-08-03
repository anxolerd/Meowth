import os
from unittest.mock import patch
from flask import url_for
from config import BASEDIR
from project.models import Vacancy, City, Category
from project.tests.utils import ProjectTestCase
from bs4 import BeautifulSoup


class TestFeedView(ProjectTestCase):

    def test_vacancy(self):
        vacancy = Vacancy.query.first()
        url = url_for('feed.get_vacancy', name_in_url=vacancy.name_in_url)
        with self.client as client:
            resp = client.get(url, follow_redirects=True)
            self.assertIn(vacancy.title, resp.data.decode())
            self.assertIn(vacancy.text, resp.data.decode())

    def get_vacancy_with_csrf(self):
        vacancy = Vacancy.query.first()
        url = url_for('feed.get_vacancy', name_in_url=vacancy.name_in_url)
        resp = self.client.get(url, follow_redirects=True)
        soup = BeautifulSoup(resp.data, 'html.parser')
        csrf_token = soup.find(id='csrf_token')['content']
        return csrf_token, url

    @patch('project.tasks.mail.celery_send_mail.delay')
    def test_not_completed_form(self, send_mail):
        csrf_token, url = self.get_vacancy_with_csrf()

        attachment = os.path.join(BASEDIR, 'project/tests/test_feed.py')
        new_resp = self.client.post(
            url+'form', data=dict(
                csrf_token=csrf_token,
                name='',
                email='',
                phone='',
                comment='',
                attachment=open(attachment, 'rb')
            ), content_type='multipart/form-data'
        )
        self.assertFalse(new_resp.json['success'])
        self.assertIsNotNone(new_resp.json['name'])
        self.assertIsNotNone(new_resp.json['email'])
        self.assertIsNotNone(new_resp.json['phone'])
        self.assertIsNotNone(new_resp.json['attachment'])
        self.assertEqual(send_mail.call_count, 0)

    @patch('project.tasks.mail.celery_send_mail.delay')
    def test_completed_form(self, send_mail):
        csrf_token, url = self.get_vacancy_with_csrf()

        attachment = os.path.join(BASEDIR, 'requirements.txt')
        new_resp = self.client.post(
            url+'form', data=dict(
                csrf_token=csrf_token,
                name='spam',
                email='spam@gmail.com',
                phone='0931234567',
                comment='',
                attachment=open(attachment, 'rb')
            ), content_type='multipart/form-data'
        )
        self.assertTrue(new_resp.json['success'])
        self.assertFalse('name' in new_resp.json)
        self.assertFalse('email' in new_resp.json)
        self.assertFalse('phone' in new_resp.json)
        self.assertFalse('attachment' in new_resp.json)
        self.assertEqual(send_mail.call_count, 2)

    def test_vacancies_json(self):
        url = url_for('feed.json_vacancies')
        resp = self.client.get(url)
        cities = resp.json['cities']
        categories = resp.json['categories']
        vacancies = resp.json['vacancies']

        self.assertEqual(cities, [c.as_dict() for c in City.query.all()])
        self.assertEqual(
            categories,
            [c.as_dict() for c in Category.query.all()]
        )
        self.assertEqual(
            vacancies,
            [v.as_dict() for v in Vacancy.bl.get_visible()]
        )