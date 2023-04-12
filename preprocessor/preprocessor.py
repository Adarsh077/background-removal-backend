import os
from . import process_pdf
from . import process_text

supported_file = ['.png', '.jpg', '.jpeg', '.pdf', '.txt']


def process(file):
    file_path = 'files/' + file.filename

    _, file_extension = os.path.splitext(file_path)

    try:
        supported_file.index(file_extension)
    except:
        os.remove('files/' + file.filename)
        print('Unsupported file')
        return []

    if file_extension == '.pdf':
        return process_pdf.procress_pdf(file)

    if file_extension == '.txt':
        return process_text.procress_text(file)

    return [file_path]
