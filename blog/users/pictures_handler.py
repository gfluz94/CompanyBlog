import os
from PIL import Image
from flask import current_app, url_for

def add_profile_pic(pic_upload, username):

    filename = pic_upload.filename
    ext_type = filename.split(".")[-1]
    storage_filename = username+"."+ext_type
    file_path = os.path.join(os.getcwd(), "blog/users/static/profile_pics", storage_filename)
    output_size = (200,200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(file_path)
    return storage_filename