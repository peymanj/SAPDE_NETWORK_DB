from __future__ import print_function
from genericpath import isfile
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from os import path, getenv
from source.framework.pool import Pool
from source.framework.utilities import log


class GoogleSheetsAPI(object):
    def __init__(self, sheet_id=None, sheet_name=None, cred_path=None):
        self.cred_path = cred_path

    def check_creds(self):
        if not isfile(path.join(self.cred_path, 'google_sheet.json')):
            return FileNotFoundError
        return self.initiate_service()

    def initiate_service(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
        SAMPLE_RANGE_NAME = 'Class Data!A2:E'
        token_path = path.join(self.cred_path, 'token.json')

        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    path.join(self.cred_path, 'google_sheet.json'), SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w+') as token:
                token.write(creds.to_json())
        try:
            self.sheet_service = build('sheets', 'v4', credentials=creds)
        except:
            DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
            self.sheet_service = build('sheets', 'v4', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        try:
            self.drive_service = build('drive', 'v3', credentials=creds)
        except:
            DISCOVERY_SERVICE_URL = 'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'
            self.drive_service = build('drive', 'v3', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        return True

        # sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                             range=SAMPLE_RANGE_NAME).execute()
        # values = result.get('values', [])
        # if not values:
        #     print('No data found.')
        # else:
        #     print('Name, Major:')
        #     for row in values:
        #         # Print columns A and E, which correspond to indices 0 and 4.
        #         print('%s, %s' % (row[0], row[4]))

    def create(self, title):
        service = self.sheet_service
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
        return spreadsheet.get('spreadsheetId')

    def batch_update(self, spreadsheet_id, title, find, replacement):
        service = self.sheet_service
        # [START sheets_batch_update]
        requests = []
        # Change the spreadsheet's title.
        requests.append({
            'updateSpreadsheetProperties': {
                'properties': {
                    'title': title
                },
                'fields': 'title'
            }
        })
        # Find and replace text
        requests.append({
            'findReplace': {
                'find': find,
                'replacement': replacement,
                'allSheets': True
            }
        })
        # Add additional requests (operations) ...

        body = {
            'requests': requests
        }
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()
        find_replace_response = response.get('replies')[1].get('findReplace')
        # print('{0} replacements made.'.format(
        #     find_replace_response.get('occurrencesChanged')))
        # [END sheets_batch_update]
        return response

    def get_values(self, spreadsheet_id, range_name):
        service = self.sheet_service
        # [START sheets_get_values]
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        # print('{0} rows retrieved.'.format(len(rows)))
        # [END sheets_get_values]
        return result

    def batch_get_values(self, spreadsheet_id, _range_names):
        service = self.sheet_service
        # [START sheets_batch_get_values]
        range_names = [
            # Range names ...
        ]
        # [START_EXCLUDE silent]
        range_names = _range_names
        # [END_EXCLUDE]
        result = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id, ranges=range_names).execute()
        ranges = result.get('valueRanges', [])
        # print('{0} ranges retrieved.'.format(len(ranges)))
        # [END sheets_batch_get_values]
        return result

    def update_values(self, spreadsheet_id, range_name, value_input_option,
                      _values):
        service = self.sheet_service
        # [START sheets_update_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
        # [END sheets_update_values]
        return result

    def batch_update_values(self, spreadsheet_id, range_name,
                            value_input_option, _values):
        service = self.sheet_service
        # [START sheets_batch_update_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        data = [
            {
                'range': range_name,
                'values': values
            },
            # Additional ranges to update ...
        ]
        body = {
            'valueInputOption': value_input_option,
            'data': data
        }
        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
        # [END sheets_batch_update_values]
        return result

    def format_cells(self, spreadsheet_id, format_dict):
        service = self.sheet_service
        result = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                    body=format_dict).execute()

    def append_values(self, spreadsheet_id, range_name, value_input_option,
                      _values):
        service = self.sheet_service
        # [START sheets_append_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells appended.'.format(result \
                                           .get('updates') \
                                           .get('updatedCells')))
        # [END sheets_append_values]
        return result

    def pivot_tables(self, spreadsheet_id):
        service = self.sheet_service
        # Create two sheets for our pivot table.
        body = {
            'requests': [{
                'addSheet': {}
            }, {
                'addSheet': {}
            }]
        }
        batch_update_response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        source_sheet_id = batch_update_response.get('replies')[0] \
            .get('addSheet').get('properties').get('sheetId')
        target_sheet_id = batch_update_response.get('replies')[1] \
            .get('addSheet').get('properties').get('sheetId')
        requests = []
        # [START sheets_pivot_tables]
        requests.append({
            'updateCells': {
                'rows': {
                    'values': [
                        {
                            'pivotTable': {
                                'source': {
                                    'sheetId': source_sheet_id,
                                    'startRowIndex': 0,
                                    'startColumnIndex': 0,
                                    'endRowIndex': 20,
                                    'endColumnIndex': 7
                                },
                                'rows': [
                                    {
                                        'sourceColumnOffset': 1,
                                        'showTotals': True,
                                        'sortOrder': 'ASCENDING',

                                    },

                                ],
                                'columns': [
                                    {
                                        'sourceColumnOffset': 4,
                                        'sortOrder': 'ASCENDING',
                                        'showTotals': True,

                                    }
                                ],
                                'values': [
                                    {
                                        'summarizeFunction': 'COUNTA',
                                        'sourceColumnOffset': 4
                                    }
                                ],
                                'valueLayout': 'HORIZONTAL'
                            }
                        }
                    ]
                },
                'start': {
                    'sheetId': target_sheet_id,
                    'rowIndex': 0,
                    'columnIndex': 0
                },
                'fields': 'pivotTable'
            }
        })
        body = {
            'requests': requests
        }
        response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        # [END sheets_pivot_tables]
        return response

    def conditional_formatting(self, spreadsheet_id):
        service = self.sheet_service

        # [START sheets_conditional_formatting]
        my_range = {
            'sheetId': 0,
            'startRowIndex': 1,
            'endRowIndex': 11,
            'startColumnIndex': 0,
            'endColumnIndex': 4,
        }
        requests = [{
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [my_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{
                                'userEnteredValue':
                                    '=GT($D2,median($D$2:$D$11))'
                            }]
                        },
                        'format': {
                            'textFormat': {
                                'foregroundColor': {'red': 0.8}
                            }
                        }
                    }
                },
                'index': 0
            }
        }, {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [my_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{
                                'userEnteredValue':
                                    '=LT($D2,median($D$2:$D$11))'
                            }]
                        },
                        'format': {
                            'backgroundColor': {
                                'red': 1,
                                'green': 0.4,
                                'blue': 0.4
                            }
                        }
                    }
                },
                'index': 0
            }
        }]
        body = {
            'requests': requests
        }
        response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        print('{0} cells updated.'.format(len(response.get('replies'))))
        # [END sheets_conditional_formatting]
        return response

    def filter_views(self, spreadsheet_id):
        service = self.sheet_service

        # [START sheets_filter_views]
        my_range = {
            'sheetId': 0,
            'startRowIndex': 0,
            'startColumnIndex': 0,
        }
        addFilterViewRequest = {
            'addFilterView': {
                'filter': {
                    'title': 'Sample Filter',
                    'range': my_range,
                    'sortSpecs': [{
                        'dimensionIndex': 3,
                        'sortOrder': 'DESCENDING'
                    }],
                    'criteria': {
                        0: {
                            'hiddenValues': ['Panel']
                        },
                        6: {
                            'condition': {
                                'type': 'DATE_BEFORE',
                                'values': {
                                    'userEnteredValue': '4/30/2016'
                                }
                            }
                        }
                    }
                }
            }
        }

        body = {'requests': [addFilterViewRequest]}
        addFilterViewResponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        duplicateFilterViewRequest = {
            'duplicateFilterView': {
                'filterId':
                    addFilterViewResponse['replies'][0]['addFilterView']['filter']
                    ['filterViewId']
            }
        }

        body = {'requests': [duplicateFilterViewRequest]}
        duplicateFilterViewResponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        updateFilterViewRequest = {
            'updateFilterView': {
                'filter': {
                    'filterViewId': duplicateFilterViewResponse['replies'][0]
                    ['duplicateFilterView']['filter']['filterViewId'],
                    'title': 'Updated Filter',
                    'criteria': {
                        0: {},
                        3: {
                            'condition': {
                                'type': 'NUMBER_GREATER',
                                'values': {
                                    'userEnteredValue': '5'
                                }
                            }
                        }
                    }
                },
                'fields': {
                    'paths': ['criteria', 'title']
                }
            }
        }

        body = {'requests': [updateFilterViewRequest]}
        updateFilterViewResponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        # [END sheets_filter_views]

    def grant_access(self, sheet_id, email):
        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print("Permission Id: %s" % response.get('id'))

        batch = self.drive_service.new_batch_http_request(callback=callback)
        # user_permission = {
        #     'type': 'user',
        #     'role': 'writer',
        #     'emailAddress': 'user@example.com'
        # }
        # batch.add(self.drive_service.permissions().create(
        #         fileId=sheet_id,
        #         body=user_permission,
        #         fields='id',
        # ))
        domain_permission = {
            'type': 'user',
            'role': 'reader',
            'emailAddress': email,
        }
        batch.add(self.drive_service.permissions().create(
            fileId=sheet_id,
            body=domain_permission,
            fields='id',
        ))
        batch.execute()
