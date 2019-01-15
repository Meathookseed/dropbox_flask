import json
import unittest
from flask_testing import TestCase
from flask import current_app
from app import create_app
from app.api.service.auth import AuthService
from app.api.service.user import UserService
from app.extensions import db
from app.shortcuts import dbsession


class Test(TestCase):

    def create_app(self):
        self.app, socket = create_app('test_config.yaml')
        self.app.config['TESTING'] = True
        return self.app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        dbsession.remove()
        db.drop_all()


class TestAdminUser(Test):

    @staticmethod
    def create_admin_user():

        data = {'username': 'test', 'password': 'test', "email": "test", "admin": True}
        UserService.create(data=data)

        response = AuthService.login({'username': 'test', 'password': 'test'})

        token = json.loads(response.data)['token']

        return token

    @staticmethod
    def create_not_admin_user():
        data = {'username': 'test2', 'password': 'test', "email": "test2", "admin": False}
        UserService.create(data=data)

        response = AuthService.login({'username': 'test2', 'password': 'test'})

        token = json.loads(response.data)['token']

        return token

    def test_user_list(self):

        token = TestAdminUser.create_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/', headers={'Bearer': f'{token}'})

            self.assertEqual(response.status_code, 200)

        token = TestAdminUser.create_not_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/', headers={'Bearer': f'{token}'})

            self.assertEqual(response.status_code, 403)

    def test_user_retrieve(self):

        token = TestAdminUser.create_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/1/', headers={'Bearer': f'{token}'})

        self.assertEqual(response.status_code, 200)

        token = TestAdminUser.create_not_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/1/', headers={'Bearer': f'{token}'})

        self.assertEqual(response.status_code, 403)

    def test_user_delete(self):

        token = TestAdminUser.create_admin_user()

        with self.app.test_client() as client:
            response = client.delete('/user/1/', headers={'Bearer': f'{token}'})
            self.assertEqual(response.status_code, 200)

        token = TestAdminUser.create_not_admin_user()

        with self.app.test_client() as client:
            response = client.delete('/user/1/', headers={'Bearer': f'{token}'})

        self.assertEqual(response.status_code, 403)

    def test_user_update(self):

        token = TestAdminUser.create_admin_user()

        with self.app.test_client() as client:

            response = client.patch('/user/1/', headers={'Bearer': f'{token}'},
                                    data=json.dumps({"username": "updated",
                                                     "password": "1234",
                                                     "email": "test3",
                                                     "admin": False}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

        with self.app.test_client() as client:
            response = client.patch('/user/1/', headers={'Bearer': f'{token}'})

        self.assertEqual(response.status_code, 204)

        token = TestAdminUser.create_not_admin_user()

        with self.app.test_client() as client:
            response = client.patch('/user/1/', headers={'Bearer': f'{token}'},
                                    data=json.dumps({"username": "updated"}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 403)

    def test_user_create(self):

        with self.app.test_client() as client:
            response = client.post('/registration/', data=json.dumps({"username": "test",
                                                                      "password": "test",
                                                                      "email": "test",
                                                                      "admin": True}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

        with self.app.test_client() as client:
            response = client.post('/registration/',)

        self.assertEqual(response.status_code, 204)


# class TestNotAdminUser(Test):
#
#     @staticmethod
#     def create_not_admin_user():
#
#         data = {'username': 'test2', 'password': 'test', "email": "test2", "admin": False}
#         UserService.create(data=data)
#
#         response = AuthService.login({'username': 'test2', 'password': 'test'})
#         print(response.data)
#         token = json.loads(response.data)['token']
#
#         return token
#
#     def test_user_list(self):
#
#         token = TestNotAdminUser.create_not_admin_user()
#
#         with self.app.test_client() as client:
#             response = client.get('/user/', headers={'Bearer': f'{token}'})
#
#             self.assertEqual(response.status_code, 403)
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
