from flask_socketio import emit

from app import create_app
from app.api.serializers import UserSchema, VaultSchema
from app.api.service import UserService, VaultService

app, socket = create_app(config_file='config.yaml')


@socket.on('vault_events')
def __handle_vault_events(json: dict):
    user = UserService.one(**json)

    emit('vault_state', UserSchema().dump(user).data)


@socket.on('file_events')
def __handle_file_events(json: dict):
    vault = VaultService.one(**json)
    emit('file_state', VaultSchema().dump(vault).data)


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port='5000', debug=True)
