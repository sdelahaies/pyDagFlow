import pdftotext

def pdf2text(input:dict) -> dict:
    filename = input["FileInput"]['filename']
    try:
        with open(f"../uploads/{filename}", "rb") as f:
            pdf = pdftotext.PDF(f)
            return {'text': "\n\n".join(pdf)}
    except Exception as e:
        return {'error': str(e)}
