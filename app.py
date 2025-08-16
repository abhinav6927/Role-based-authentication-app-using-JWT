from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password or len(password) < 8:
            return {'message': 'Invalid input'}, 400
        if User.query.filter_by(username=username).first():
            return {'message': 'Username exists'}, 400
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Registered successfully'}, 200

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            token = create_access_token(identity=user.id)
            return {
                'access_token': token,
                'username': user.username,
                'role': user.role
            }, 200
        return {'message': 'Invalid credentials'}, 401

class AllUsers(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {'message': 'Unauthorized'}, 403
        users = User.query.all()
        result = []
        for u in users:
            result.append({
                'id': u.id,
                'username': u.username,
                'role': u.role,
                'created_at': u.created_at.strftime('%Y-%m-%d %H:%M')
            })
        return result, 200

class CreateUser(Resource):
    @jwt_required()
    def post(self):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)
        if admin.role != 'admin':
            return {'message': 'Unauthorized'}, 403
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        if not username or not password or role not in ['admin', 'student']:
            return {'message': 'Invalid input'}, 400
        if User.query.filter_by(username=username).first():
            return {'message': 'Username exists'}, 400
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created'}, 200

class DeleteUser(Resource):
    @jwt_required()
    def delete(self, user_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)
        if admin.role != 'admin':
            return {'message': 'Unauthorized'}, 403
        target = User.query.get(user_id)
        if not target:
            return {'message': 'User not found'}, 404
        db.session.delete(target)
        db.session.commit()
        return {'message': 'User deleted'}, 200

class ChangePassword(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        current = data.get('current_password')
        new = data.get('new_password')
        confirm = data.get('confirm_password')
        user = User.query.get(user_id)
        if not user or user.password != current:
            return {'message': 'Wrong current password'}, 401
        if new != confirm or len(new) < 8:
            return {'message': 'Invalid new password'}, 400
        user.password = new
        db.session.commit()
        return {'message': 'Password changed'}, 200

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(AllUsers, '/users')
api.add_resource(CreateUser, '/create-user')
api.add_resource(DeleteUser, '/users/<int:user_id>')
api.add_resource(ChangePassword, '/change-password')

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', password='admin123', role='admin')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
