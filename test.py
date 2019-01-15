import json
import unittest
from flask_testing import TestCase
from app import create_app
from app.api.service.auth import AuthService
from app.api.service.user import UserService
from app.api.service.vault import VaultService
from app.extensions import db
from app.shortcuts import dbsession
from app.models.models import User
from app.api.decorators.token import token_required

class Test(TestCase):

    def create_app(self):
        self.app, socket = create_app('test_config.yaml')
        return self.app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        dbsession.remove()
        db.drop_all()


class TestUser(Test):

    @staticmethod
    def user_create():
        data = {'username': 'test', 'password': 'test', "email": "test"}
        UserService.create(data=data)
        info = AuthService.login({'username': 'test', 'password': 'test'})
        for content in info.__dict__['response']:
            token = json.loads(content)
            return token['token']

    def test_user_list(self):
        token = TestUser.user_create()
        with self.app.test_client() as client:
            users = client.get('/user/', headers={'Bearer': f'{token}'})
            data = json.loads(users.data)
        self.assertIn('users', data)

    def test_user_retrieve(self):

        token = TestUser.user_create()

        with self.app.test_client() as client:
            users = client.get('/user/1/', headers={'Bearer': f'{token}'})
            data = json.loads(users.data)

        self.assertIn('user', data)

    def test_user_delete(self):

        token = TestUser.user_create()

        with self.app.test_client() as client:
            client.delete('/user/1/', headers={'Bearer': f'{token}'})

        self.assert200('Deleted', 200)

    def test_user_update(self):

        token = TestUser.user_create()

        with self.app.test_client() as client:
            users = client.patch('/user/1/', headers={'Bearer': f'{token}'}, data=json.dumps({"username": "updated"}),
                                 content_type='application/json')

            data = json.loads(users.data)

        self.assertIn('user updated', data['message'])

    def test_user_create(self):

        with self.app.test_client() as client:
            users = client.post('/registration/', data=json.dumps({"username": "test",
                                                                  "password": "test",
                                                                   "email": "test"}),
                                content_type='application/json')

            data = json.loads(users.data)

        self.assertIn('token', data)


# class TestVault(Test):
#
#     @staticmethod
#     def vault_create():
#
#         data = {'username': 'test', 'password': 'test', "email": "test"}
#         UserService.create(data=data)
#         vault = {'title': 'test_vault', 'description': 'test'}
#
#         VaultService.create(data=vault, id=1)
#
#         info = AuthService.login({'username': 'test', 'password': 'test'})
#
#         for content in info.__dict__['response']:
#             token = json.loads(content)
#             return token['token']
#
#     def test_vault_list(self):
#
#         token = TestVault.vault_create()
#
#         with self.app.test_client() as client:
#
#             vaults = client.get('/vault/user_1/', headers={'Bearer': f"{token}"})
#
#             data = json.loads(vaults.data)
#
#         self.assertIn('vaults', data)


if __name__ == '__main__':
    unittest.main()
