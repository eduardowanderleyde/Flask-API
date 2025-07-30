from marshmallow import Schema, fields, validate
from datetime import datetime


class CategorySchema(Schema):
    """Schema for category validation."""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    color = fields.Str(default="#3B82F6")
    icon = fields.Str(default="💰")
    user_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TransactionSchema(Schema):
    """Schema for transaction validation."""
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(['income', 'expense']))
    category_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    date = fields.Date(default=datetime.now().date)
    notes = fields.Str(allow_none=True)
    category_name = fields.Str(dump_only=True)
    category_color = fields.Str(dump_only=True)
    category_icon = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class FinancialGoalSchema(Schema):
    """Schema for financial goal validation."""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    target_amount = fields.Float(required=True)
    current_amount = fields.Float(default=0)
    deadline = fields.Date(allow_none=True)
    description = fields.Str(allow_none=True)
    user_id = fields.Int(dump_only=True)
    is_active = fields.Bool(default=True)
    progress = fields.Float(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TransactionSummarySchema(Schema):
    """Schema for transaction summary."""
    total_income = fields.Float(dump_only=True)
    total_expense = fields.Float(dump_only=True)
    balance = fields.Float(dump_only=True)
    period = fields.Str(dump_only=True)
    transactions_count = fields.Int(dump_only=True) 