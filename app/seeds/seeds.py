from app.models.userRoleModel import User, Role
from app.config.connector import db  # Import db from extensions.py

def seed_data():
    admin_role = Role(name='Admin')
    user_role = Role(name='User')

    admin_user = User(username='admin', email='admin@example.com')
    admin_user.set_password('adminpassword')
    admin_user.roles = [admin_role]

    regular_user = User(username='user', email='user@example.com')
    regular_user.set_password('userpassword')
    regular_user.roles = [user_role]

    db.session.add(admin_role)
    db.session.add(user_role)
    db.session.add(admin_user)
    db.session.add(regular_user)
    db.session.commit()
