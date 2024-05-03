def get_doc_mime_type(filename:str) -> str:
    if filename.endswith('.pdf'):
        return 'application/pdf'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        return 'image/jpeg'
    elif filename.endswith('.doc') or filename.endswith('.docx'):
        return 'application/msword'
    elif filename.endswith('.json'):
        return 'application/json'
    elif filename.endswith('.csv'):
        return 'text/csv'
    elif filename.endswith('.txt'):
        return 'text/plain'