#!/usr/bin/python
from configparser import ConfigParser
import os
from werkzeug.utils import secure_filename
from lib.persistence.config_persistence import config

UPLOAD_FOLDER = config("assets/database/database.ini", "upload")["folder"]
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



def save_image(file):
    print("Saving image:" + file.filename)
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return filename
