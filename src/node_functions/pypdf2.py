from PyPDF2 import PdfReader

def pypdf2(input:dict) -> dict:
    filename = input["FileInput"]['filename']
    try:
        pdf = PdfReader(f"../uploads/{filename}")
        text='\n'
        for page in pdf.pages:
            text += page.extract_text() + '\n'
        return {'text': text}
    except Exception as e:
        return {'error': str(e)}