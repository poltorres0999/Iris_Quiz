from flask import Flask, session, render_template
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
sess = Session()
sess.init_app(app)

from models.iris_real_like_response import RealLikeResponse
import views.iris_quiz_form
import views.upload_iris_image_form
import views.iris_quiz_statistics
import views.iris_responses

@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
import views