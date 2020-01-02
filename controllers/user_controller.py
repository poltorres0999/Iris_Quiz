from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from models.user import User


class UserController:

    def store_new_user(self, username, email, password):
        password_hash = generate_password_hash(password)
        # todo: store new user to db

    def autenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password, password):
            return None
        else:
            return user


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
