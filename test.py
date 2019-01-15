import json
import unittest
from flask_testing import TestCase
from app import create_app
from app.api.service.auth import AuthService
from app.api.service.user import UserService
from app.extensions import db
from app.shortcuts import dbsession
from app.api.service.vault import VaultService


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


class TestUser(Test):

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

        token = TestUser.create_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/', headers={'Bearer': '{}'.format(token)})

            self.assertEqual(response.status_code, 200)

        token = TestUser.create_not_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/', headers={'Bearer': '{}'.format(token)})

            self.assertEqual(response.status_code, 403)

    def test_user_retrieve(self):

        token = TestUser.create_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/1/', headers={'Bearer': '{}'.format(token)})

        self.assertEqual(response.status_code, 200)

        token = TestUser.create_not_admin_user()

        with self.app.test_client() as client:

            response = client.get('/user/1/', headers={'Bearer': '{}'.format(token)})

        self.assertEqual(response.status_code, 403)

    def test_user_delete(self):

        token = TestUser.create_admin_user()

        with self.app.test_client() as client:
            response = client.delete('/user/1/', headers={'Bearer': '{}'.format(token)})
            self.assertEqual(response.status_code, 200)

        token = TestUser.create_not_admin_user()

        with self.app.test_client() as client:
            response = client.delete('/user/1/', headers={'Bearer': '{}'.format(token)})

        self.assertEqual(response.status_code, 403)

    def test_user_update(self):

        token = TestUser.create_admin_user()

        with self.app.test_client() as client:

            response = client.patch('/user/1/', headers={'Bearer': '{}'.format(token)},
                                    data=json.dumps({"username": "updated",
                                                     "password": "1234",
                                                     "email": "test3",
                                                     "admin": False}),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

        with self.app.test_client() as client:
            response = client.patch('/user/1/', headers={'Bearer': '{}'.format(token)})

        self.assertEqual(response.status_code, 204)

        token = TestUser.create_not_admin_user()

        with self.app.test_client() as client:
            response = client.patch('/user/1/', headers={'Bearer': '{}'.format(token)},
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


class TestVault(Test):

    @staticmethod
    def create_user():
        data = {'username': 'test2', 'password': 'tes2t', "email": "test2", "admin": True}
        UserService.create(data=data)

        response = AuthService.login({'username': 'test2', 'password': 'tes2t'})

        token = json.loads(response.data)['token']

        return token

    @staticmethod
    def create_vault():

        data = {'username': 'test', 'password': 'test', "email": "test", "admin": True}
        UserService.create(data=data)

        response = AuthService.login({'username': 'test', 'password': 'test'})

        token = json.loads(response.data)['token']

        app = Test().create_app()

        with app.test_client() as client:

            client.post('/vault/1/', headers={'Bearer': "{}".format(token)},
                        data=json.dumps({'title': 'test', 'description': 'test'}),
                        content_type='application/json')

        return token

    def test_create_vault(self):

        token = TestVault.create_vault()

        with self.app.test_client() as client:

            response = client.post('/vault/1/', headers={'Bearer': "{}".format(token)})

        self.assertEqual(response.status_code, 204)

        with self.app.test_client() as client:

            response = client.post('/vault/1/', headers={'Bearer': "{}".format(token)},
                                   data=json.dumps({'title': 'test', 'description': 'test'}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

        with self.app.test_client() as client:

            response = client.post('/vault/2/', headers={'Bearer': "{}".format(token)},
                                   data=json.dumps({'title': 'test', 'description': 'test'}),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 403)

    def test_vault_list(self):

        token = TestVault.create_vault()

        with self.app.test_client() as client:

            response = client.get('/vault/user_1/', headers={'Bearer': "{}".format(token)})

            self.assertEqual(response.status_code, 200)

        with self.app.test_client() as client:

            response = client.get('/vault/user_3/', headers={'Bearer': "{}".format(token)})

            self.assertEqual(response.status_code, 403)

    def test_vault_retrieve(self):

        token = TestVault.create_vault()

        with self.app.test_client() as client:
            response = client.get('/vault/1/', headers={'Bearer': "{}".format(token)})

            self.assertEqual(response.status_code, 200)

        with self.app.test_client() as client:

            response = client.get('/vault/2/', headers={'Bearer': "{}".format(token)})

            self.assertEqual(response.status_code, 403)

    def test_vault_update(self):

        token = TestVault.create_vault()

        with self.app.test_client() as client:

            response = client.patch('/vault/1/', headers={'Bearer': "{}".format(token)},
                                    data=json.dumps({'title': 'test2', 'description': 'test2'}),
                                    content_type='application/json')

            self.assertEqual(response.status_code, 200)

        # TODO Need to create 2 users with 2 vaults to check 403 error
        # with self.app.test_client() as client:
        #
        #     response = client.patch('/vault/2/', headers={'Bearer': "{}".format(token)},
        #                             data=json.dumps({'title': 'test2', 'description': 'test2'}),
        #                             content_type='application/json')
        #
        #     self.assertEqual(response.status_code, 403)

        token = TestVault.create_user()

        with self.app.test_client() as client:
            response = client.patch('/vault/2/', headers={'Bearer': "{}".format(token)},
                                    data=json.dumps({'title': 'test2', 'description': 'test2'}),
                                    content_type='application/json')

            self.assertEqual(response.status_code, 204)

    def test_vault_delete(self):

        token = TestVault.create_vault()

        with self.app.test_client() as client:

            response = client.delete('/vault/1/', headers={'Bearer': '{}'.format(token)})

        self.assertEqual(response.status_code, 200)

        token = TestVault.create_user()

        with self.app.test_client() as client:

            response = client.delete('/vault/1/', headers={'Bearer': '{}'.format(token)})

        self.assertEqual(response.status_code, 204)

        # TODO Need to create 2 users with 2 vaults to check 403 error


if __name__ == '__main__':
    unittest.main()
