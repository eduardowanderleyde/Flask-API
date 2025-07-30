from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.routes import api_bp
from app.models.user import User, db
from app.schemas.user import UserRegisterSchema, UserLoginSchema, UserSchema
from marshmallow import ValidationError


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        # Validate input data
        schema = UserRegisterSchema()
        data = schema.load(request.get_json())
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Return user data (without password)
        user_schema = UserSchema()
        return jsonify({
            'message': 'User registered successfully',
            'user': user_schema.dump(user)
        }), 201
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT tokens."""
    try:
        # Validate input data
        schema = UserLoginSchema()
        data = schema.load(request.get_json())
        
        # Find user
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is disabled'}), 401
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({'error': 'Validation error', 'details': e.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': new_access_token
    }), 200


@api_bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': user.to_dict()
    }), 200 