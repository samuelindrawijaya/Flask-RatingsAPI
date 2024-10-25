from app import db
from app.models.userRoleModel import Role

class RoleDAL:
    @staticmethod
    def create_role(name):
        role = Role(name=name)
        db.session.add(role)
        db.session.commit()
        return role

    @staticmethod
    def get_role_by_id(role_id):
        return db.session.get(Role, role_id)

    @staticmethod
    def get_role_by_name(name):
        return Role.query.filter_by(name=name).first()

    @staticmethod
    def update_role(role_id, new_name):
        role = db.session.get(Role, role_id)
        if role:
            role.name = new_name
            db.session.commit()
        return role

    @staticmethod
    def delete_role(role_id):
        role = db.session.get(Role, role_id)
        if role:
            db.session.delete(role)
            db.session.commit()
            return True
        return False

    @staticmethod
    def list_roles():
        return Role.query.all()
