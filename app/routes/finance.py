from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes import api_bp
from app.models.finance import Category, Transaction, FinancialGoal, TransactionType
from app.schemas.finance import CategorySchema, TransactionSchema, FinancialGoalSchema
from app.models.user import db
from datetime import datetime, date, timedelta


# Schemas
category_schema = CategorySchema()
transaction_schema = TransactionSchema()
goal_schema = FinancialGoalSchema()


# ==================== CATEGORIES ====================

@api_bp.route('/finance/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all categories for the current user."""
    current_user_id = get_jwt_identity()
    categories = Category.query.filter_by(user_id=current_user_id).all()
    return jsonify({
        'message': 'Categories retrieved successfully',
        'categories': [category.to_dict() for category in categories]
    }), 200


@api_bp.route('/finance/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create a new category."""
    current_user_id = get_jwt_identity()
    
    try:
        data = request.get_json()
        data['user_id'] = current_user_id
        
        category = Category(**data)
        db.session.add(category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ==================== TRANSACTIONS ====================

@api_bp.route('/finance/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get all transactions for the current user."""
    current_user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=current_user_id).order_by(Transaction.date.desc()).all()
    
    return jsonify({
        'message': 'Transactions retrieved successfully',
        'transactions': [transaction.to_dict() for transaction in transactions]
    }), 200


@api_bp.route('/finance/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create a new transaction."""
    current_user_id = get_jwt_identity()
    
    try:
        data = request.get_json()
        data['user_id'] = current_user_id
        
        # Validate category belongs to user
        category = Category.query.filter_by(id=data['category_id'], user_id=current_user_id).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        transaction = Transaction(**data)
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/finance/transactions/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    """Delete a transaction."""
    current_user_id = get_jwt_identity()
    
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    db.session.delete(transaction)
    db.session.commit()
    
    return jsonify({'message': 'Transaction deleted successfully'}), 200


# ==================== SUMMARY ====================

@api_bp.route('/finance/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """Get financial summary for the current user."""
    current_user_id = get_jwt_identity()
    
    # Get current month transactions
    today = date.today()
    start = date(today.year, today.month, 1)
    if today.month == 12:
        end = date(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(today.year, today.month + 1, 1) - timedelta(days=1)
    
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user_id,
        Transaction.date >= start,
        Transaction.date <= end
    ).all()
    
    # Calculate summary
    total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
    total_expense = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
    balance = total_income - total_expense
    
    return jsonify({
        'message': 'Summary retrieved successfully',
        'summary': {
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'balance': float(balance),
            'transactions_count': len(transactions)
        }
    }), 200


# ==================== GOALS ====================

@api_bp.route('/finance/goals', methods=['GET'])
@jwt_required()
def get_goals():
    """Get all financial goals for the current user."""
    current_user_id = get_jwt_identity()
    goals = FinancialGoal.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'message': 'Goals retrieved successfully',
        'goals': [goal.to_dict() for goal in goals]
    }), 200


@api_bp.route('/finance/goals', methods=['POST'])
@jwt_required()
def create_goal():
    """Create a new financial goal."""
    current_user_id = get_jwt_identity()
    
    try:
        data = request.get_json()
        data['user_id'] = current_user_id
        
        goal = FinancialGoal(**data)
        db.session.add(goal)
        db.session.commit()
        
        return jsonify({
            'message': 'Goal created successfully',
            'goal': goal.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 