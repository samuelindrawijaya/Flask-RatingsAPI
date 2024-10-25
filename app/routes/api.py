from flask import Blueprint
from flask_login import login_required
from app.controllers.user_controller import UserController
from app.controllers.auth_controller import AuthController
from app.controllers.role_controller import RoleController
from app.controllers.review_controller import ReviewController
from app.utils.jwtdecorator import token_required, admin_required

user_bp = Blueprint('users', __name__)
role_bp = Blueprint('roles', __name__)
auth_bp = Blueprint('auth', __name__)
review_bp = Blueprint('reviews', __name__)

# Route for user login
auth_bp.add_url_rule('/login',  view_func=AuthController.login, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=AuthController.logout, methods=['POST'])
auth_bp.add_url_rule('/profile', view_func=login_required((AuthController.profile)), methods=['GET'])

# User Routes
user_bp.add_url_rule('/',              view_func=login_required(token_required(UserController.get_all_users)), methods=['GET'])
user_bp.add_url_rule('/<int:user_id>', view_func=login_required(token_required(admin_required(UserController.get_user_by_id))), methods=['GET'])
user_bp.add_url_rule('/',              view_func=login_required(token_required(admin_required(UserController.add_user))), methods=['POST'])
user_bp.add_url_rule('/<int:user_id>', view_func=login_required(token_required(admin_required(UserController.update_user))), methods=['PUT'])
user_bp.add_url_rule('/<int:user_id>', view_func=login_required(token_required(admin_required(UserController.delete_user))), methods=['DELETE'])

# Role Routes
role_bp.add_url_rule('/',              view_func=login_required(token_required(admin_required(RoleController.get_all_roles))), methods=['GET'])
role_bp.add_url_rule('/<int:role_id>', view_func=login_required(token_required(admin_required(RoleController.get_role_by_id))), methods=['GET'])
role_bp.add_url_rule('/',              view_func=login_required(token_required(admin_required(RoleController.add_role))), methods=['POST'])
role_bp.add_url_rule('/<int:role_id>', view_func=login_required(token_required(admin_required(RoleController.update_role))), methods=['PUT'])
role_bp.add_url_rule('/<int:role_id>', view_func=login_required(token_required(admin_required(RoleController.delete_role))), methods=['DELETE'])

# Review Routes
review_bp.add_url_rule('/',                view_func=login_required(token_required(admin_required(ReviewController.get_all_reviews))), methods=['GET'])
review_bp.add_url_rule('/<int:review_id>', view_func=login_required(token_required(admin_required(ReviewController.get_review_by_id))), methods=['GET'])
review_bp.add_url_rule('/',                view_func=login_required(token_required(admin_required(ReviewController.add_review))), methods=['POST'])
review_bp.add_url_rule('/<int:review_id>', view_func=login_required(token_required(admin_required(ReviewController.update_review))), methods=['PUT'])
review_bp.add_url_rule('/<int:review_id>', view_func=login_required(token_required(admin_required(ReviewController.delete_review))), methods=['DELETE'])