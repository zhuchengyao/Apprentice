"""add billing tables (subscription_plans, user_subscriptions, credit_balances, credit_transactions) and user_id to api_usage

Revision ID: i4d6e8f1a2b3
Revises: h3c5d7e9f1a3
Create Date: 2026-04-09 12:00:00.000000

"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "i4d6e8f1a2b3"
down_revision: Union[str, None] = "h3c5d7e9f1a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Pre-defined plan UUIDs for seeding
FREE_PLAN_ID = "00000000-0000-0000-0000-000000000101"
BASIC_PLAN_ID = "00000000-0000-0000-0000-000000000102"
PRO_PLAN_ID = "00000000-0000-0000-0000-000000000103"


def upgrade() -> None:
    # 1. subscription_plans
    op.create_table(
        "subscription_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(50), unique=True, nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("monthly_credits", sa.Integer(), nullable=False),
        sa.Column("price_usd", sa.Float(), nullable=False),
        sa.Column("stripe_price_id", sa.String(200), nullable=True),
        sa.Column("features", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )

    # 2. user_subscriptions
    op.create_table(
        "user_subscriptions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("subscription_plans.id"), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="active"),
        sa.Column("stripe_subscription_id", sa.String(200), nullable=True),
        sa.Column("stripe_customer_id", sa.String(200), nullable=True),
        sa.Column("current_period_start", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("current_period_end", sa.DateTime(), nullable=False, server_default=sa.text("now() + interval '30 days'")),
        sa.Column("cancel_at_period_end", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )
    op.create_unique_constraint("uq_user_subscriptions_user_id", "user_subscriptions", ["user_id"])
    op.create_index("ix_user_subscriptions_user_id", "user_subscriptions", ["user_id"])

    # 3. credit_balances
    op.create_table(
        "credit_balances",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("balance", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )
    op.create_unique_constraint("uq_credit_balances_user_id", "credit_balances", ["user_id"])
    op.create_index("ix_credit_balances_user_id", "credit_balances", ["user_id"])

    # 4. credit_transactions
    op.create_table(
        "credit_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("balance_after", sa.Integer(), nullable=False),
        sa.Column("transaction_type", sa.String(50), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("reference_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    )
    op.create_index("ix_credit_transactions_user_id", "credit_transactions", ["user_id"])
    op.create_index("ix_credit_transactions_created_at", "credit_transactions", ["created_at"])
    op.create_index("ix_credit_transactions_type", "credit_transactions", ["transaction_type"])

    # 5. Add user_id to api_usage
    op.add_column("api_usage", sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key("fk_api_usage_user_id", "api_usage", "users", ["user_id"], ["id"], ondelete="SET NULL")
    op.create_index("ix_api_usage_user_id", "api_usage", ["user_id"])

    # 6. Seed subscription plans
    free_features = json.dumps({"max_books": 1, "allowed_models": ["claude-haiku-4-5-20251001", "gpt-5.4-mini", "gpt-5.4-nano"], "priority_processing": False})
    basic_features = json.dumps({"max_books": 5, "allowed_models": None, "priority_processing": False})
    pro_features = json.dumps({"max_books": None, "allowed_models": None, "priority_processing": True})

    op.execute(
        f"""
        INSERT INTO subscription_plans (id, name, display_name, monthly_credits, price_usd, features)
        VALUES
            ('{FREE_PLAN_ID}', 'free', 'Free', 500, 0.0, '{free_features}'),
            ('{BASIC_PLAN_ID}', 'basic', 'Basic', 15000, 9.99, '{basic_features}'),
            ('{PRO_PLAN_ID}', 'pro', 'Pro', 50000, 29.99, '{pro_features}')
        ON CONFLICT (name) DO NOTHING
        """
    )

    # 7. Backfill existing users: create credit_balances and user_subscriptions
    op.execute(
        f"""
        INSERT INTO credit_balances (id, user_id, balance)
        SELECT gen_random_uuid(), id, 500
        FROM users
        WHERE id NOT IN (SELECT user_id FROM credit_balances)
        """
    )
    op.execute(
        f"""
        INSERT INTO user_subscriptions (id, user_id, plan_id, status)
        SELECT gen_random_uuid(), id, '{FREE_PLAN_ID}', 'active'
        FROM users
        WHERE id NOT IN (SELECT user_id FROM user_subscriptions)
        """
    )


def downgrade() -> None:
    op.drop_index("ix_api_usage_user_id", table_name="api_usage")
    op.drop_constraint("fk_api_usage_user_id", "api_usage", type_="foreignkey")
    op.drop_column("api_usage", "user_id")

    op.drop_table("credit_transactions")
    op.drop_table("credit_balances")
    op.drop_table("user_subscriptions")
    op.drop_table("subscription_plans")
