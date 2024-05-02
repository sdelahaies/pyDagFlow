from .utils import get_doc_mime_type
import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('TESSERACT_URL')
endpoint = os.getenv('TESSERACT_ENDPOINT')
url = "http://apitesseract:8000/tesseract"

def tesseract(input:dict) -> dict:
    filename = input['FileInput']['filename']
    try:
        
        headers = {'accept': 'application/json'}
        content_type = get_doc_mime_type(filename)
        files = {'file': (input, open(f'./uploads/{input}', 'rb'), content_type)} 
        response = requests.post(
            f'{url}/{endpoint}', headers=headers, files=files)
        output = response.json()
        print(output)
        return output
    except Exception as e:
        return {'error': str(e)}