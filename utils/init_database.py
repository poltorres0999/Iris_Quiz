import os
import shutil
from datetime import datetime
from random import randint, choice
from werkzeug.security import generate_password_hash
import app
import config
from app import db
from models.iris_image import IrisImage
from models.user import User
from models.iris_real_like_response import RealLikeResponse
from models.iris_real_syn_response import RealSynResponse

R_IMG_WIDTH = 320
R_IMG_HEIGHT = 280
S_IMG_WIDTH = 64
S_IMG_HEIGHT = 64
REAL_V = "real"
SYN_V = "synthetic"

r_s_injection_folder = "C:/Users/polto/Desktop/injection/real"
s_injection_folder ="C:/Users/polto/Desktop/injection/syn"

r_store_path = os.path.join(config.basedir, app.Config.REAL_IMG_STORE_PATH)
s_store_path = os.path.join(config.basedir, app.Config.SYNTHETIC_IMG_STORE_PATH)
s_r_store_path = app.Config.REAL_IMG_STORE_PATH
s_s_store_path = app.Config.SYNTHETIC_IMG_STORE_PATH

NUM_USERS = 5

def inject_images(src_folder, dest_folder, server_store_path, img_w, img_h, img_type):
    file_names = os.listdir(src_folder)
    for file_name in file_names:
        full_file_name = os.path.join(src_folder, file_name)
        img_store_path = os.path.join(dest_folder, file_name)
        server_img_store_path = os.path.join(server_store_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, img_store_path)
            db.session.add(IrisImage(width=img_w, height=img_h, store_path=server_img_store_path, file_name=file_name,
                                     type=img_type))
            db.session.commit()


def create_fake_quiz_responses():
    # get real images from database
    real_images = db.session.query(IrisImage).filter_by(type='real').all()
    # get fake images from database
    synthetic_images = db.session.query(IrisImage).filter_by(type='synthetic').all()
    # join real and fake images
    all_images = real_images + synthetic_images
    # foreach image create a random RealLikeResponse
    total_responses = 0
    date = datetime.now().isoformat()
    # foreach each image create a random response
    for img in all_images:
        fake_responses = [randint(1, 5) for i in range(5)]
        total_responses += sum(fake_responses)
        if RealLikeResponse.query.get(img.id) is None:
            db.session.add(RealLikeResponse(iris_image_id=img.id, date=date))
        db.session.query(RealLikeResponse).filter_by(iris_image_id=img.id).update(
            {'surely_real': fake_responses[0],
             'maybe_real': fake_responses[1],
             'indecise': fake_responses[2],
             'maybe_syn': fake_responses[3],
             'surely_syn': fake_responses[4],
             'date': date})
    # foreach pair of real/synthetic images (chosen randomly) create a random response
    num_real_images = len(real_images)
    num_syn_images = len(synthetic_images)
    for i in range(total_responses):
        real_image = real_images[randint(0, num_real_images - 1)]
        syn_image = synthetic_images[randint(0, num_syn_images - 1)]
        db.session.add(RealSynResponse(real_image_id=real_image.id, syn_image_id=syn_image.id,
                                       real_image_response=choice(["real", "synthetic"]),
                                       syn_image_response=choice(["real", "synthetic"]),
                                       date=date))
    db.session.commit()


def create_mock_users():
    usernames = [f"user_{i}" for i in range(NUM_USERS)]
    passwords = [generate_password_hash(f"user_pass_{i}") for i in range(NUM_USERS)]
    mails = [f"user_mail_{i}@gmail.com" for i in range(NUM_USERS)]

    for i in range(NUM_USERS):
        db.session.add(User(username=usernames[i], password=passwords[i], email=mails[i]))
    db.session.commit()

def main():
    # Load real images to the server local storage
    #inject_images(r_s_injection_folder, r_store_path, s_r_store_path, R_IMG_WIDTH, R_IMG_HEIGHT, REAL_V)
    print("Real images injected")
    # Load synthetic images to the server local storage
    #inject_images(s_injection_folder, s_store_path, s_s_store_path, S_IMG_WIDTH, S_IMG_HEIGHT, SYN_V)
    print("Synthetic images injected")
    # Create fake responses
    #create_fake_quiz_responses()
    print("Mock responses created")
    create_mock_users()


if __name__ == "__main__":
    main()
