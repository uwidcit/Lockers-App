import os, string, random
from werkzeug.utils import secure_filename

## Ask if we should randomize files names, we can always store the orignal in the DB and mask that from the user

def store_file(file):
    file.save(os.path.join('Uploaded_Files', file.filename))