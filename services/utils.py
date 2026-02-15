import os
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

def allowed_file(filename: str) -> bool:
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_upload(file_storage) -> str:
    filename = secure_filename(file_storage.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file_storage.save(filepath)
    return filepath
