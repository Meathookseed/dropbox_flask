
DOCS_PARAMS_FOR_TOKEN = {'Bearer': {"description": "Custom HTTP header which contains the token",
                                    "in": "header",
                                    "type": "string",
                                    "required": False}}

DOCS_PARAMS_FOR_PHOTO = {'Bearer': {"description": "Custom HTTP header which contains the token",
                                    "in": "header",
                                    "type": "string",
                                    "required": False},
                         'Photo': {"description": "User upload its own photo",
                                                  "in": "header",
                                                  "type": "file",
                                                  "required": False}}

DOCS_PARAMS_FOR_FILE = {'Bearer': {"description": "Custom HTTP header which contains the token",
                                    "in": "header",
                                    "type": "string",
                                    "required": False},
                        'File': {"description": "File Upload",
                                                  "in": "header",
                                                  "type": "file",
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
