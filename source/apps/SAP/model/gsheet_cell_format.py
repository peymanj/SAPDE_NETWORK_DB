centered = {"requests":
    [
        {
            "repeatCell":
                {
                    "cell":
                        {
                            "userEnteredFormat":
                                {
                                    "horizontalAlignment": "CENTER",
                                    #   'backgroundColorStyle':{
                                    #       "themeColor": 'ACCENT4'
                                    #   }
                                }
                        }
                    ,
                    "fields": "userEnteredFormat(horizontalAlignment)",
                    "range":
                        {
                            "sheetId": 0,
                            #   "rowIndex": 2,
                            #   "columnIndex": 2,
                            #   "startRowIndex": 3,
                            #   "endRowIndex": 10
                            #   "startColumnIndex": 5,
                            #   "endColumnIndex": 20
                        }
                }
        }
    ]
}

header_merge = {"requests":
    [
        {
            'mergeCells':
                {
                    'mergeType': 'MERGE_ALL',
                    'range':
                        {
                            'sheetId': 0,
                            'startRowIndex': 0,
                            'endRowIndex': 1,
                            'startColumnIndex': 0,
                            'endColumnIndex': 8
                        }
                }
        },
        {
            "repeatCell": {
                "range": {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 44
                },
                "cell":
                    {
                        "userEnteredFormat":
                            {
                                "backgroundColor":
                                    {
                                        "red": 0.0,
                                        "green": 0.0,
                                        "blue": 0.0
                                    },
                                "textFormat": {
                                    "foregroundColor": {
                                        "red": 1.0,
                                        "green": 1.0,
                                        "blue": 1.0
                                    },
                                    "fontSize": 12,
                                    "bold": 'true'
                                }
                            }
                    },
                "fields": "userEnteredFormat"
            }
        }
    ]
}

order_data_bg_color = {"requests":
    [
        {
            "repeatCell":
                {
                    "cell":
                        {
                            "userEnteredFormat":
                                {
                                    'backgroundColorStyle':
                                        {
                                            "rgbColor": {
                                                "red": 0.917,
                                                "green": 0.976,
                                                "blue": 0.984
                                            }
                                        }
                                }
                        }
                    ,
                    "fields": "userEnteredFormat",
                    "range":
                        {
                            "sheetId": 0,
                            "startRowIndex": 1,
                            "endRowIndex": 4,
                            "startColumnIndex": 0,
                            "endColumnIndex": 44
                        }
                }
        }
    ]
}

order_data_dates = {"requests":
    [
        {
            "repeatCell":
                {
                    "cell":
                        {
                            "userEnteredFormat":
                                {
                                    'backgroundColorStyle':
                                        {
                                            "rgbColor": {
                                                "red": 0.917,
                                                "green": 0.976,
                                                "blue": 0.984
                                            }
                                        },
                                    'numberFormat':
                                        {
                                            "type": "DATE",
                                            "pattern": "yyyy-mm-dd"
                                        },
                                }
                        }
                    ,
                    "fields": "userEnteredFormat",
                    "range":
                        {
                            "sheetId": 0,
                            "startRowIndex": 2,
                            "endRowIndex": 4,
                            "startColumnIndex": 1,
                            "endColumnIndex": 2
                        }
                }
        }
    ]
}



# order_detail_header_back = {"requests":
#     [
#         {
#             "repeatCell":
#                 {
#                     "cell":
#                         {
#                             "userEnteredFormat":
#                                 {
#                                     'backgroundColorStyle':
#                                         {
#                                             "rgbColor": {
#                                                 "red": 0.984,
#                                                 "green": 0.933,
#                                                 "blue": 0.576
#                                             }
#                                         }
#                                 }
#                         }
#                     ,
#                     "fields": "userEnteredFormat",
#                     "range":
#                         {
#                             "sheetId": 0,
#                             "startRowIndex": 4,
#                             "endRowIndex": 6,
#                             "startColumnIndex": 23,
#                             "endColumnIndex": 40
#                         }
#                 }
#         },
#         {
#             'mergeCells':
#                 {
#                     'mergeType': 'MERGE_COLUMNS',
#                     'range':
#                         {
#                             "sheetId": 0,
#                             "startRowIndex": 3,
#                             "endRowIndex": 4,
#                             "startColumnIndex": 23,
#                             "endColumnIndex": 40
#                         }
#                 }
#         }
#     ]
# }

order_detail_header_general_start = {"requests":
    [
        {
            "repeatCell":
                {
                    "cell":
                        {
                            "userEnteredFormat":
                                {
                                    'backgroundColorStyle':
                                        {
                                            "rgbColor": {
                                                "red": 0.580,
                                                "green": 1.0,
                                                "blue": 0.788
                                            }
                                        }
                                }
                        }
                    ,
                    "fields": "userEnteredFormat",
                    "range":
                        {
                            "sheetId": 0,
                            "startRowIndex": 5,
                            "endRowIndex": 6,
                            "startColumnIndex": 0,
                            "endColumnIndex": 6
                        }
                }
        }
    ]
}

format_list = [
    header_merge,
    order_data_bg_color,
    order_data_dates,
    order_detail_header_general_start,
    centered,
]
def get_part_header_format(start_col, end_col, r, g, b):
    return  {"requests":
                [
                    {
                        "repeatCell":
                            {
                                "cell":
                                    {
                                        "userEnteredFormat":
                                            {
                                                'backgroundColorStyle':
                                                    {
                                                        "rgbColor": {
                                                            "red": r, #0.984,
                                                            "green": g, #0.792,
                                                            "blue": b, #0.576
                                                        }
                                                    } #,
                                                # 'textRotation':
                                                #     {
                                                #         "angle": -90
                                                #     }
                                            }
                                    }
                                ,
                                "fields": "userEnteredFormat",
                                "range":
                                    {
                                        "sheetId": 0,
                                        "startRowIndex": 4,
                                        "endRowIndex": 6,
                                        "startColumnIndex": start_col,
                                        "endColumnIndex": end_col,
                                    }
                            }
                    },
                    {
                        'mergeCells':
                            {
                                'mergeType': 'MERGE_COLUMNS',
                                'range':
                                    {
                                        'sheetId': 0,
                                        'startRowIndex': 3,
                                        'endRowIndex': 4,
                                        'startColumnIndex': 6,
                                        'endColumnIndex': 23,
                                    }
                            }
                    }
                ]
            }

def get_end_header_format(start_col, end_col, r, g, b):
    return {"requests":
                [
                    {
                        "repeatCell":
                            {
                                "cell":
                                    {
                                        "userEnteredFormat":
                                            {
                                                'backgroundColorStyle':
                                                    {
                                                        "rgbColor": {
                                                            "red": r, #0.580,
                                                            "green": g, # 0.776,
                                                            "blue": b, #1.0
                                                        }
                                                    }
                                            }
                                    }
                                ,
                                "fields": "userEnteredFormat",
                                "range":
                                    {
                                        "sheetId": 0,
                                        "startRowIndex": 5,
                                        "endRowIndex": 6,
                                        "startColumnIndex": start_col,
                                        "endColumnIndex": end_col
                                    }
                            }
                    }
                ]
            }