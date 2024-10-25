from flask import jsonify, request
from app.DAL.role_Dal import RoleDAL

class RoleController:
    from flask import jsonify, request
from app.DAL.role_Dal import RoleDAL

class RoleController:
    @staticmethod
    def get_all_roles():
        """
        Get all roles
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        responses:
          200:
            description: A list of roles
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: Role ID
                    example: 1
                  name:
                    type: string
                    description: Role name
                    example: "Admin"
          500:
            description: Internal Server Error
        """
        roles = RoleDAL.list_roles()
        return jsonify([role.to_dict() for role in roles]), 200

    @staticmethod
    def get_role_by_id(role_id):
        """
        Get role by ID
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: role_id
            in: path
            required: true
            schema:
              type: integer
              example: 1
        responses:
          200:
            description: Role found
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: Role ID
                  example: 1
                name:
                  type: string
                  description: Role name
                  example: "Admin"
          404:
            description: Role not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role not found"
        """
        role = RoleDAL.get_role_by_id(role_id)
        if role:
            return jsonify(role.to_dict()), 200
        return jsonify({'message': 'Role not found'}), 404

    @staticmethod
    def add_role():
        """
        Add a new role
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: role
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Role name
                  example: "Admin"
        responses:
          201:
            description: Role created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role 'Admin' created successfully."
                role:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: Role ID
                      example: 1
                    name:
                      type: string
                      description: Role name
                      example: "Admin"
          400:
            description: Role name is required
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role name is required"
        """
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': 'Role name is required'}), 400

        role = RoleDAL.create_role(data['name'])
        return jsonify({
            'message': f"Role '{data['name']}' created successfully.",
            'role': role.to_dict()
        }), 201

    @staticmethod
    def update_role(role_id):
        """
        Update a role
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: role_id
            in: path
            required: true
            schema:
              type: integer
              example: 1
          - name: role
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: Role name
                  example: "User"
        responses:
          200:
            description: Role updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role 'User' updated successfully."
                role:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: Role ID
                      example: 1
                    name:
                      type: string
                      description: Role name
                      example: "User"
          400:
            description: Role name is required
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role name is required"
          404:
            description: Role not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role not found"
        """
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': 'Role name is required'}), 400

        role = RoleDAL.update_role(role_id, data['name'])
        if role:
            return jsonify({
                'message': f"Role '{data['name']}' updated successfully.",
                'role': role.to_dict()
            }), 200
        return jsonify({'message': 'Role not found'}), 404

    @staticmethod
    def delete_role(role_id):
        """
        Delete a role
        ---
        tags:
          - Roles
        security:
          - bearerAuth: []
        parameters:
          - name: role_id
            in: path
            required: true
            schema:
              type: integer
              example: 1
        responses:
          200:
            description: Role deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role deleted successfully."
          404:
            description: Role not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Role not found"
        """
        deleted = RoleDAL.delete_role(role_id)
        if deleted:
            return jsonify({'message': 'Role deleted successfully.'}), 200
        return jsonify({'message': 'Role not found'}), 404

