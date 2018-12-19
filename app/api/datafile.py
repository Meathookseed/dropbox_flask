from app.api.service.datafile import DataFileService

from flask import request

from flask_classy import FlaskView

from flask_apispec.annotations import doc


class DataView(FlaskView):

    @doc(description='handle file update, <id> - file prop')
    def put(self, id):
        datafile = request.files['file']
        return DataFileService.create(id=id, datafile=datafile)
