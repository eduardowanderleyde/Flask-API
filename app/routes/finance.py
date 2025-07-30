from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.routes import api_bp
from app.models.finance import Category, Transaction, FinancialGoal, TransactionType
from app.schemas.finance import CategorySchema, TransactionSchema, FinancialGoalSchema, TransactionSummarySchema
from app.models.user import db
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_
import calendar


# Schemas
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)
goal_schema = FinancialGoalSchema()
goals_schema = FinancialGoalSchema(many=True)
summary_schema = TransactionSummarySchema()


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
        data = category_schema.load(request.get_json())
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


@api_bp.route('/finance/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update a category."""
    current_user_id = get_jwt_identity()
    
    category = Category.query.filter_by(id=category_id, user_id=current_user_id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    try:
        data = category_schema.load(request.get_json(), partial=True)
        
        for key, value in data.items():
            setattr(category, key, value)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Category updated successfully',
            'category': category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/finance/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete a category."""
    current_user_id = get_jwt_identity()
    
    category = Category.query.filter_by(id=category_id, user_id=current_user_id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    # Check if category has transactions
    if category.transactions:
        return jsonify({'error': 'Cannot delete category with transactions'}), 400
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted successfully'}), 200


# ==================== TRANSACTIONS ====================

@api_bp.route('/finance/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get all transactions for the current user with optional filters."""
    current_user_id = get_jwt_identity()
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category_id = request.args.get('category_id', type=int)
    transaction_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Build query
    query = Transaction.query.filter_by(user_id=current_user_id)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if transaction_type:
        query = query.filter_by(type=TransactionType(transaction_type))
    
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    # Order by date (newest first)
    query = query.order_by(Transaction.date.desc(), Transaction.created_at.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    transactions = pagination.items
    
    return jsonify({
        'message': 'Transactions retrieved successfully',
        'transactions': [transaction.to_dict() for transaction in transactions],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200


@api_bp.route('/finance/transactions', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create a new transaction."""
    current_user_id = get_jwt_identity()
    
    try:
        data = transaction_schema.load(request.get_json())
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


@api_bp.route('/finance/transactions/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    """Update a transaction."""
    current_user_id = get_jwt_identity()
    
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user_id).first()
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    try:
        data = transaction_schema.load(request.get_json(), partial=True)
        
        # Validate category if provided
        if 'category_id' in data:
            category = Category.query.filter_by(id=data['category_id'], user_id=current_user_id).first()
            if not category:
                return jsonify({'error': 'Category not found'}), 404
        
        for key, value in data.items():
            setattr(transaction, key, value)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction updated successfully',
            'transaction': transaction.to_dict()
        }), 200
        
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


# ==================== SUMMARY & REPORTS ====================

@api_bp.route('/finance/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """Get financial summary for the current user."""
    current_user_id = get_jwt_identity()
    
    # Get query parameters
    period = request.args.get('period', 'month')  # month, week, year
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Calculate date range
    today = date.today()
    if period == 'week':
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
    elif period == 'year':
        start = date(today.year, 1, 1)
        end = date(today.year, 12, 31)
    else:  # month
        start = date(today.year, today.month, 1)
        if today.month == 12:
            end = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(today.year, today.month + 1, 1) - timedelta(days=1)
    
    if start_date:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Get transactions in date range
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user_id,
        Transaction.date >= start,
        Transaction.date <= end
    ).all()
    
    # Calculate summary
    total_income = sum(t.amount for t in transactions if t.type == TransactionType.INCOME)
    total_expense = sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
    balance = total_income - total_expense
    
    # Get category breakdown
    category_breakdown = {}
    for transaction in transactions:
        category_name = transaction.category.name if transaction.category else 'Uncategorized'
        if category_name not in category_breakdown:
            category_breakdown[category_name] = {'income': 0, 'expense': 0}
        
        if transaction.type == TransactionType.INCOME:
            category_breakdown[category_name]['income'] += float(transaction.amount)
        else:
            category_breakdown[category_name]['expense'] += float(transaction.amount)
    
    return jsonify({
        'message': 'Summary retrieved successfully',
        'summary': {
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'balance': float(balance),
            'period': period,
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'transactions_count': len(transactions),
            'category_breakdown': category_breakdown
        }
    }), 200


# ==================== GOALS ====================

@api_bp.route('/finance/goals', methods=['GET'])
@jwt_required()
def get_goals():
    """Get all financial goals for the current user."""
    current_user_id = get_jwt_identity()
    
    goals = FinancialGoal.query.filter_by(user_id=current_user_id).order_by(FinancialGoal.created_at.desc()).all()
    
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
        data = goal_schema.load(request.get_json())
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


@api_bp.route('/finance/goals/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(goal_id):
    """Update a financial goal."""
    current_user_id = get_jwt_identity()
    
    goal = FinancialGoal.query.filter_by(id=goal_id, user_id=current_user_id).first()
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404
    
    try:
        data = goal_schema.load(request.get_json(), partial=True)
        
        for key, value in data.items():
            setattr(goal, key, value)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Goal updated successfully',
            'goal': goal.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/finance/goals/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(goal_id):
    """Delete a financial goal."""
    current_user_id = get_jwt_identity()
    
    goal = FinancialGoal.query.filter_by(id=goal_id, user_id=current_user_id).first()
    if not goal:
        return jsonify({'error': 'Goal not found'}), 404
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'message': 'Goal deleted successfully'}), 200 