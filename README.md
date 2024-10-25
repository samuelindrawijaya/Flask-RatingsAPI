# Flask User Management and Review Application

## Overview
This application allows users to manage their accounts and interact with review data. It includes basic user authentication and role-based authorization for specific functionalities.

## Features
### Application Functionality
- **User List**: Users can fetch a list of registered users.
- **User Registration**: Users can register an account with a username, email, and password.
- **User Login**: Registered users can log in to access additional functionalities.
- **Review Management** (Admin Only): Authorized users, such as admins, can create, update, and delete review data.
- **User Logout**: Users can log out of the application securely.

### Technical Implementation
- **Flask Framework**: The application is built using Flask, a lightweight web framework.
- **MySQL Database**: It connects to a MySQL database and uses SQLAlchemy to manage user data through models.
- **Authentication & Authorization**: Routes are protected based on the user’s authentication and role, ensuring access control to critical features like review management.
