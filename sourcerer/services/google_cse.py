import pprint
from googleapiclient.discovery import build

from sourcerer import app


def get_cse_results():
    service = build('customsearch', 'v1', developerKey=app.config['CSE_API_KEY'])

    res = service.cse().list(
        cx=app.config['CSE_CONTEXT'],
        q='nodejs video streaming server'
    ).execute()
    return res
