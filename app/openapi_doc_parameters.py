
DOCS_PARAMS_FOR_TOKEN = {'Bearer': {"description": "Custom HTTP header which contains the token",
                                    "in": "header",
                                    "type": "string",
                                    "required": False}}

GET_CODES = {'403': {'description': 'No permission'}}

POST_CODES = {'403': {'description': 'No permission'},
              '200': {'description': 'Created'},
              '204': {'description': 'No data'}}

PATCH_CODES = {'403': {'description': 'No permission'},
               '200': {'description': 'Updated'},
               '204': {'description': 'No data'}}

DELETE_CODES = {'200': {'description': 'Deleted'},
                '403': {'description': 'No permission'}}
