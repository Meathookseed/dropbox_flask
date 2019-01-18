import json
import unittest
from flask_testing import TestCase
from app import create_app
from app.api.service import AuthService, UserService
from app.extensions import db
from app.shortcuts import dbsession

import io


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

        with self.app.test_client() as client:

            response = client.get('/user/2/', headers={'Bearer': '{}'.format(token)})

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


class TestPhoto(Test):

    @staticmethod
    def create_user():
        data = {'username': 'test', 'password': 'test', "email": "test", "admin": True}
        UserService.create(data=data)

        response = AuthService.login({'username': 'test', 'password': 'test'})

        token = json.loads(response.data)['token']

        return token

    def test_create_photo(self):

        token = TestPhoto.create_user()

        with self.app.test_client() as client:

            data = dict()

            data['photo'] = (io.BytesIO(b"abcdef"), 'test.jpg')

            response = client.put('/photo/1/', headers={'Bearer': '{}'.format(token)},
                                  data=data,
                                  content_type='multipart/form-data')

            self.assertEqual(response.status_code, 200)

            data = dict()

            data['photo'] = (io.BytesIO(b"abcdef"), 'test.jpg')

            response = client.put('/photo/2/', headers={'Bearer': '{}'.format(token)},
                                  data=data,
                                  content_type='multipart/form-data')

            self.assertEqual(response.status_code, 403)


class TestLogin(Test):

    @staticmethod
    def create_user():
        data = {'username': 'test', 'password': 'test', "email": "test", "admin": True}
        UserService.create(data=data)

    def test_login(self):
        TestLogin.create_user()

        with self.app.test_client() as client:

            response = client.post('/login/', data=json.dumps({'username': 'test',
                                                               'password': 'test'}),
                                   content_type='application/json')

            self.assertEqual(response.status_code, 200)

            response = client.post('/login/', data=json.dumps({}),
                                   content_type='application/json')

            self.assertEqual(response.status_code, 401)

            response = client.post('/login/', data=json.dumps({'username2': 'test',
                                                               'password': 'test'}),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 401)

            response = client.post('/login/', data=json.dumps({'username': 'test2',
                                                               'password': 'test2'}),
                                   content_type='application/json')

            self.assertEqual(response.status_code, 401)

            response = client.post('/login/', data=json.dumps({'username': 'test',
                                                               'password': 'test2'}),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 401)


class TestToken(Test):

    def test_token(self):

        with self.app.test_client() as client:

            response = client.get('/user/')

            self.assertEqual(response.status_code, 401)

            token = TestUser.create_admin_user()

            response = client.get('/user/?Bearer={}'.format(token))

            self.assertEqual(response.status_code, 200)


class TestFile(Test):

    @staticmethod
    def fixture():
        data = {'username': 'test', 'password': 'test', "email": "test", "admin": True}
        UserService.create(data=data)

        response = AuthService.login({'username': 'test', 'password': 'test'})

        token = json.loads(response.data)['token']

        app = Test().create_app()

        with app.test_client() as client:

            client.post('/vault/1/', headers={'Bearer': "{}".format(token)},
                        data=json.dumps({'title': 'test', 'description': 'test'}),
                        content_type='application/json')

            client.post('/file/1/', headers={'Bearer': '{}'.format(token)},
                        data=json.dumps({"name": "first file", "description": "fixture"}),
                        content_type='application/json')

        return token

    @staticmethod
    def fixture_without_file_create():
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

    def test_file_create(self):

        token = TestFile.fixture_without_file_create()

        with self.app.test_client() as client:

            response = client.post('/file/1/', headers={'Bearer': '{}'.format(token)},
                                   data=json.dumps({"name": "first file", "description": "fixture"}),
                                   content_type='application/json')
            self.assertEqual(response.status_code, 200)

            response = client.post('/file/2/',headers={'Bearer': '{}'.format(token)},
                                   data=json.dumps({"name": "first file", "description": "fixture"}),
                                   content_type='application/json')

            self.assertEqual(response.status_code, 403)

    def test_file_list(self):

        token = TestFile.fixture()

        with self.app.test_client() as client:

            response = client.get('/file/vault_1/', headers={"Bearer": "{}".format(token)})

            self.assertEqual(response.status_code, 200)

            response = client.get('/file/vault_2/', headers={"Bearer": "{}".format(token)})

            self.assertEqual(response.status_code, 403)

    def test_file_retrieve(self):

        token = TestFile.fixture()

        with self.app.test_client() as client:

            response = client.get('/file/1/', headers={"Bearer": "{}".format(token)})

            self.assertEqual(response.status_code, 200)

            response = client.get('/file/2/', headers={"Bearer": "{}".format(token)})

            self.assertEqual(response.status_code, 403)

    def test_file_update(self):

        token = TestFile.fixture()

        with self.app.test_client() as client:

            response = client.patch('/file/1/', headers={'Bearer': "{}".format(token)},
                                    data=json.dumps({"name": "updated", "description": "updated"}),
                                    content_type='application/json')
            self.assertEqual(response.status_code, 200)

            response = client.patch('/file/2/', headers={'Bearer': "{}".format(token)},
                                    data=json.dumps({"name": "updated", "description": "updated"}),
                                    content_type='application/json')

            self.assertEqual(response.status_code, 403)

    def test_file_delete(self):
        token = TestFile.fixture()

        with self.app.test_client() as client:

            response = client.delete('/file/1/', headers={'Bearer': "{}".format(token)})

            self.assertEqual(response.status_code, 200)

            response = client.delete('/file/2/', headers={'Bearer': "{}".format(token)})

            self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
