import datetime
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from flask_login import login_user, logout_user, current_user
import jwt
from app.DAL.user_Dal import UserDAL


class AuthController:
    @staticmethod
    def login():
        """
        Login a user and return both a session login and a JWT token.
        ---
        tags:
          - Authentication
        summary: User login
        description: Login user and returns both a session-based login and a JWT access token.
        parameters:
          - in: body
            name: user
            description: The email and password for login.
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  example: "testuser@example.com"
                password:
                  type: string
                  example: "password123"
        responses:
          200:
            description: Successful login, returns an access token.
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
          401:
            description: Invalid credentials
        """
        data = request.get_json()

       
        user = UserDAL.get_user_by_email(data['email'])
        if user and user.check_password(data['password']):
            # Log the user in with session-based authentication
            login_user(user)
            # using flask_jwt_extended    
            access_token = create_access_token(  
                identity={'user_id': user.id, 'role': user.roles[0].name},  # Assuming user has a list of roles
                expires_delta=datetime.timedelta(hours=1)  # Set token expiry time
            )
            
            return jsonify({
                'message': 'Logged in successfully',
                'access_token': access_token
            }), 200

        return jsonify({'message': 'Invalid credentials'}), 401
    
    @staticmethod
    def logout():
        """
        Logout user and invalidate the JWT token.
        ---
        tags:
          - Authentication
        summary: User logout
        description: Logs out the user and invalidates the JWT access token.
        responses:
          200:
            description: Successfully logged out and token invalidated.
          403:
            description: Token missing.
        """
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Extract token from "Bearer <token>"

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        # Add the token to the blacklist to invalidate it
        #  blacklist.add(token)

        # Log out the user using Flask-Login
        logout_user()

        return jsonify({'message': 'Logged out and token invalidated successfully'}), 200
    
    
    @staticmethod
    def profile():
        """
        Get user profile
        ---
        tags:
          - Authentication
        security:
          - bearerAuth: []
        responses:
          200:
            description: User profile retrieved successfully
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: User ID
                  example: 1
                username:
                  type: string
                  description: Username of the user
                  example: "johndoe"
                email:
                  type: string
                  description: Email address of the user
                  example: "johndoe@example.com"
                roles:
                  type: array
                  items:
                    type: string
                    description: Role name
                    example: "Admin"
          401:
            description: Unauthorized - Token is invalid or missing
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Unauthorized access"
        """
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'roles': [role.name for role in current_user.roles]
        }), 200
    
    
    
    