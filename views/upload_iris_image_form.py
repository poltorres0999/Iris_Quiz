import os
from app import session
from flask import render_template, flash, redirect, request
from flask_login import login_required

from app import app
from controllers.iris_image_controller import IrisImageController
from forms.forms import UploadIrisImageForm

TITLE = "Upload iris image"
controller = IrisImageController()


@app.route("/upload_iris_image", methods=['GET'])
@login_required
def upload_image_form_get():
    form = UploadIrisImageForm()
    return render_template('upload_iris_image_form.html', form=form, title=TITLE)


@app.route("/upload_iris_image", methods=['POST'])
@login_required
def upload_image_form_post():
    session.pop('_flashes', None)
    upload_image_form = UploadIrisImageForm(request.form)
    img_width = request.form["img_width"]
    img_height = request.form["img_height"]
    img_type = request.form["img_type"]

    if upload_image_form.validate():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files_to_upload = request.files.getlist("file")

        if len(files_to_upload) == 0:
            flash('No selected file')
        else:
            if img_type == "real":
                store_path = app.config["REAL_IMG_STORE_PATH"]
            else:
                store_path = app.config["SYNTHETIC_IMG_STORE_PATH"]
            # todo: try catch
            n_files_uploaded, not_uploaded_files = upload_files(files_to_upload=files_to_upload,
                                                                store_path=store_path, img_width=img_width,
                                                                img_height=img_height, img_type=img_type)

            if not_uploaded_files == 0 or len(not_uploaded_files) > 0:

                if n_files_uploaded == 0:
                    flash(f"No files were uploaded, please check file format, allowed formats "
                          f"are {app.config['ALLOWED_EXTENSIONS']}")
                if len(not_uploaded_files) > 0:
                    flash(
                        f"{len(not_uploaded_files)} files were not uploaded, please check file format, "
                        f"allowed formats are {app.config['ALLOWED_EXTENSIONS']}")

                return redirect('/upload_iris_image')

            return render_template("index.html")


def upload_files(files_to_upload, store_path, img_width, img_height, img_type):
    not_allowed = []
    count = 0
    for file in files_to_upload:
        filename = file.filename
        if allowed_file(file.filename):
            file.save(os.path.join(store_path, filename))
            controller.store_image_data(width=img_width, height=img_height, image_type=img_type,
                                        file_name=filename, store_path=store_path)
            count += 1
        else:
            not_allowed.append(filename)
    return count, not_allowed


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
