from .utils import get_doc_mime_type
import requests

def beit(input:dict) -> dict:
    filename = input['FileInput']['filename']
    try:
        return _request_beit(filename)
    except Exception as e:
        return {'error': str(e)}


def _request_beit(filename: str) -> dict:
    url = "http://0.0.0.0:8001/classify?model=beit"
    headers = {
        'accept': 'application/json',
    }
    content_type = get_doc_mime_type(filename)
    files = {
        'file': (filename, open(f'./uploads/{filename}', 'rb'), content_type),
    }
    response = requests.post(url, headers=headers, files=files)
    output = response.json()['output']
    return {'class':output}