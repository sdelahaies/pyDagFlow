import fitz

def pymupdf(input:dict) -> dict:
    filename = input["FileInput"]['filename']
    try:
        doc = fitz.open(f"./uploads/{filename}")
        page = doc[0]
        return {'text':page.get_text()}
    except Exception as e:
        return {'error': str(e)}