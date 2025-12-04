"""Minimal Flask backend exposing /api/users and serving a Bootstrap homepage."""
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from datetime import datetime

from app.models import User
from backend.db import engine, SessionLocal

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Initialize flask-restx Api; keep docs under /docs-restx to avoid clashing with existing /docs
# mask=False disables the X-Fields header in Swagger documentation
api = Api(app, title='Test CICD API', version='0.1', doc='/docs-restx', mask=False)


# RFC 7807 Problem Details response helper
def problem_response(title: str, status: int, detail: str, instance: str = None, error_type: str = None):
    """Return a RFC 7807 compliant error response."""
    response = {
        'type': error_type or 'about:blank',
        'title': title,
        'status': status,
        'detail': detail
    }
    if instance:
        response['instance'] = instance
    return jsonify(response), status


# Error handler for unhandled exceptions (RFC 7807 format)
@app.errorhandler(Exception)
def handle_exception(error):
    """Catch all unhandled exceptions and return them as RFC 7807 JSON errors."""
    app.logger.error(f'Unhandled exception: {error}', exc_info=True)
    
    return problem_response(
        title='Internal Server Error',
        status=500,
        detail=str(error) if app.debug else 'An unexpected error occurred while processing your request',
        instance=request.path
    )


# Define a user model for documentation/serialization
user_model = api.model('User', {
    'id': fields.Integer(description='Primary key'),
    'email': fields.String(description='User email'),
    'last_logon': fields.String(description='Last logon time (ISO8601)', required=False, example=None),
    'role': fields.String(description='User role')
})

# Input model for creating/updating users (no id)
user_input = api.model('UserInput', {
    'email': fields.String(required=True, description='User email'),
    'last_logon': fields.String(required=False, description='Last logon time (ISO8601)'),
    'role': fields.String(required=False, description='User role', example='user')
})

@api.route('/api/users')
class UsersResource(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        session = SessionLocal()
        try:
            users = session.query(User).all()
            return users
        finally:
            session.close()

    @api.expect(user_input, validate=True)
    @api.response(201, 'User created')
    @api.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user."""
        payload = api.payload or {}
        email = payload.get('email')
        last_logon = payload.get('last_logon')
        role = payload.get('role') or 'user'

        dt = None
        if last_logon:
            try:
                dt = datetime.fromisoformat(last_logon)
            except Exception:
                api.abort(400, 'last_logon must be ISO8601')

        session = SessionLocal()
        try:
            new_user = User(email=email, last_logon=dt, role=role)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user, 201
        finally:
            session.close()

@api.route('/api/users/<int:user_id>')
@api.response(404, 'User not found')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        session = SessionLocal()
        try:
            user = session.get(User, user_id)
            if user is None:
                api.abort(404, 'User not found')
            return user
        finally:
            session.close()

    @api.response(204, 'User deleted')
    def delete(self, user_id):
        session = SessionLocal()
        try:
            user = session.get(User, user_id)
            if user is None:
                api.abort(404, 'User not found')
            session.delete(user)
            session.commit()
            return '', 204
        finally:
            session.close()


if __name__ == '__main__':
    # For development only. Use gunicorn / production server otherwise.
    app.run(host='0.0.0.0', port=5000, debug=True)
