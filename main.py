from app import create_app
from app.api.service.user import UserService
from app.api.serializers.user import UserSchema
from app.api.serializers.vault import VaultSchema
from app.api.service.vault import VaultService

from flask_socketio import emit

app, socket = create_app()


@socket.on('vault_events')
def __handle_vault_events(json):
    user = UserService.one(id=json['id'])
    emit('vault_state', UserSchema().dump(user).data)

@socket.on('file_events')
def __hande_file_events(json):
    print('event')
    vault = VaultService.one(id=json['id'])
    emit('file_state', VaultSchema().dump(vault).data)

if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port='5000', debug=True)
