from app import db
from app.models.userRoleModel import User,Role
from sqlalchemy.exc import IntegrityError

class UserDAL:
    @staticmethod
    def create_user(username, email, password, roles=[]):
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            if roles:
                for role_name in roles:
                    role = Role.query.filter_by(name=role_name).first()
                    if role:
                        user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            return None  # Handle unique constraint violation

    @staticmethod
    def get_user_by_id(user_id):
        return db.session.get(User, user_id)
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def update_user(user_id, new_username=None, new_email=None, new_password=None, new_roles=[]):
        user = db.session.get(User, user_id)
        if user:
            if new_username:
                user.username = new_username
            if new_email:
                user.email = new_email
            if new_password:
                user.set_password(new_password)
            if new_roles:
                user.roles.clear()  # Clear existing roles
                for role_name in new_roles:
                    role = Role.query.filter_by(name=role_name).first()
                    if role:
                        user.roles.append(role)
            db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def list_users():
        return User.query.all()
