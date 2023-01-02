# file:image_service.py

from flask import send_from_directory

# 
def get_image(repertory_path:str, image_path:str):
    return send_from_directory(repertory_path, image_path)
