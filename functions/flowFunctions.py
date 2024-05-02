from PyPDF2 import PdfReader
import requests

def fileinput(input:dict) -> dict:
    return input

def pypdf2(input:dict) -> dict:
    filename = input['FileInput']['filename']
    try:
        pdf = PdfReader(f"./uploads/{filename}")
        text='\n'
        for page in pdf.pages:
            text += page.extract_text() + '\n'
        return {'text': text}
    except Exception as e:
        return {'error': str(e)}
    
def beit(input:dict) -> dict:
    filename = input['FileInput']['filename']
    print("allo?")
    try:
        url = "http://0.0.0.0:8001/classify?model=beit"
        headers = {
            'accept': 'application/json',
        }
        # check file type
        if filename.endswith('.pdf'):
            content_type = 'application/pdf'
        elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            content_type = 'image/jpeg'
        files = {
            'file': (filename, open(f'./uploads/{filename}', 'rb'), content_type),
        }
        response = requests.post(url, headers=headers, files=files)
        output = response.json()['output']
        return {'class':output}
    except Exception as e:
        return {'error': str(e)}


def output(input:dict) -> dict:
    print(input)
    return input