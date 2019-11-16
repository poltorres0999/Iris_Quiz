import app
from app import db
import os
import shutil
from models.iris_image import IrisImage

R_IMG_WIDTH = 320
R_IMG_HEIGHT = 280
S_IMG_WIDTH = 64
S_IMG_HEIGHT = 64
REAL_V = "real"
SYN_V = "synthetic"

r_s_injection_folder = "C:/Users/polto/Desktop/injection/real"
s_injection_folder ="C:/Users/polto/Desktop/injection/syn"
r_store_path = app.Config.REAL_IMG_STORE_PATH
s_store_path = app.Config.SYNTHETIC_IMG_STORE_PATH


def inject_images(src_folder, dest_folder, img_w, img_h, img_type):
    file_names = os.listdir(src_folder)
    for file_name in file_names:
        full_file_name = os.path.join(src_folder, file_name)
        img_store_path = os.path.join(dest_folder, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, img_store_path)
            db.session.add(IrisImage(width=img_w, height=img_h, store_path=img_store_path, type=img_type))
            db.session.commit()


def main():
    inject_images(r_s_injection_folder, r_store_path, R_IMG_WIDTH, R_IMG_HEIGHT, REAL_V)
    inject_images(s_injection_folder, s_store_path, S_IMG_WIDTH, S_IMG_HEIGHT, SYN_V)


if __name__ == "__main__":
    main()