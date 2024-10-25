from flask import jsonify, request
from app.DAL.user_Dal import UserDAL

class UserController:
    @staticmethod
    def get_all_users():
        """
        Get all users
        ---
        tags:
          - Users
        security:
          - bearerAuth: []
        responses:
            200:
                description: A list of users
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: User ID
                                example: 1
                            username:
                                type: string
                                description: User username
                                example: "johndoe"
                            email:
                                type: string
                                description: User email
                                example: "johndoe@example.com"
                            roles:
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
                            created_at:
                                type: string
                                format: date-time
                                description: User creation time
                                example: "2024-10-24T12:34:56Z"
        """
        users = UserDAL.list_users()
        return jsonify([user.to_dict() for user in users]), 200

    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        ---
        tags:
          - Users
        security:
          - bearerAuth: []
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
        responses:
            200:
                description: User details
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: User ID
                            example: 1
                        username:
                            type: string
                            description: User username
                            example: "johndoe"
                        email:
                            type: string
                            description: User email
                            example: "johndoe@example.com"
                        roles:
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
                        created_at:
                            type: string
                            format: date-time
                            description: User creation time
                            example: "2024-10-24T12:34:56Z"
            404:
                description: User not found
        """
        user = UserDAL.get_user_by_id(user_id)
        if user:
            return jsonify(user.to_dict()), 200
        return jsonify({'message': 'User not found'}), 404

    @staticmethod
    def add_user():
        """
        Add a new user
        ---
        tags:
          - Users
        security:
          - bearerAuth: []
        parameters:
          - name: user
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                password:
                  type: string
                roles:
                  type: array
                  items:
                    type: string
        responses:
            201:
                description: User created
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: User ID
                            example: 1
                        username:
                            type: string
                            description: User username
                            example: "johndoe"
                        email:
                            type: string
                            description: User email
                            example: "johndoe@example.com"
                        roles:
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
            400:
                description: Missing required fields
            409:
                description: User already exists
        """
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Missing required fields'}), 400

        user = UserDAL.create_user(data['username'], data['email'], data['password'], data.get('roles', []))
        if user:
            return jsonify({
                'message': f"User {user.username} created successfully.",
                'user': user.to_dict()
            }), 201
        return jsonify({'message': 'User already exists'}), 409

    @staticmethod
    def update_user(user_id):
        """
        Update a user
        ---
        tags:
          - Users
        security:
          - bearerAuth: []
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
          - name: user
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                email:
                  type: string
                password:
                  type: string
                roles:
                  type: array
                  items:
                    type: string
        responses:
            200:
                description: User updated
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: User ID
                            example: 1
                        username:
                            type: string
                            description: User username
                            example: "johndoe"
                        email:
                            type: string
                            description: User email
                            example: "johndoe@example.com"
                        roles:
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
            400:
                description: Invalid input
            404:
                description: User not found
        """
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid input'}), 400

        user = UserDAL.update_user(user_id, data.get('username'), data.get('email'), data.get('password'), data.get('roles', []))
        if user:
            return jsonify({'message': 'User updated successfully', 'user': user.to_dict()}), 200
        return jsonify({'message': 'User not found'}), 404

    @staticmethod
    def delete_user(user_id):
        """
        Delete a user
        ---
        tags:
          - Users
        security:
          - bearerAuth: []
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
        responses:
            200:
                description: User deleted
            404:
                description: User not found
        """
        deleted = UserDAL.delete_user(user_id)
        if deleted:
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'message': 'User not found'}), 404
