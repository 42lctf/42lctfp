"""Init User

Revision ID: 9364b74e1516
Revises: 
Create Date: 2023-12-26 19:54:36.399240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '9364b74e1516'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'campus',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('intra_campus_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=True),
        sa.Column('country', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime, default=datetime.now()),
    )

    op.create_table(
        'ctf_users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password', sa.String(length=100), nullable=True),
        sa.Column('intra_user_id', sa.BigInteger(), nullable=True),
        sa.Column('nickname', sa.String(length=50), nullable=False, unique=True),
        sa.Column('description', sa.String(length=250), nullable=True),
        sa.Column('website', sa.String(length=100), nullable=True),
        sa.Column('github', sa.String(length=100), nullable=True),
        sa.Column('linkedin', sa.String(length=100), nullable=True),
        sa.Column('twitter', sa.String(length=100), nullable=True),
        sa.Column('is_admin', sa.Boolean(), default=False, nullable=False),
        sa.Column('is_hidden', sa.Boolean(), default=False, nullable=False),
        sa.Column('is_verified', sa.Boolean(), default=False, nullable=False),
        sa.Column('is_2fa_enabled', sa.Boolean(), default=False, nullable=False),
        sa.Column('tfa_token', sa.String(length=100), nullable=True),
        sa.Column('campus_id', UUID(as_uuid=True), sa.ForeignKey('campus.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'user_bans',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('ctf_users.id'), nullable=False),
        sa.Column('banned_until', sa.DateTime(), nullable=True),
        sa.Column('reason', sa.String(length=250), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'categories',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'difficulties',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'challenges',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=250), nullable=False),
        sa.Column('value', sa.Integer(), default=0, nullable=False),
        sa.Column('is_hidden', sa.Boolean, default=False, nullable=False),
        sa.Column('difficulty_id', UUID(as_uuid=True), sa.ForeignKey('difficulties.id'), nullable=False),
        sa.Column('flag', sa.String(length=100), nullable=False),
        sa.Column('flag_case_sensitive', sa.Boolean(), default=False),
        sa.Column('parent_id', UUID(as_uuid=True), sa.ForeignKey('challenges.id'), nullable=True),
        sa.Column('category_id', UUID(as_uuid=True), sa.ForeignKey('categories.id'), nullable=False),
        sa.Column('challenge_type', sa.Enum('NORMAL', 'DOCKER'), default='NORMAL', nullable=False, name='ChallengeType'),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'challenge_authors',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('challenge_id', UUID(as_uuid=True), sa.ForeignKey('challenges.id'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('ctf_users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'submissions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('challenge_id', UUID(as_uuid=True), sa.ForeignKey('challenges.id'), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('ctf_users.id'), nullable=False),
        sa.Column('content', sa.String(length=100), nullable=False),
        sa.Column("ip", sa.String(length=46), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'solves',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('ctf_users.id'), nullable=False),
        sa.Column('challenge_id', UUID, sa.ForeignKey('challenges.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'challenge_files',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('challenge_id', UUID, sa.ForeignKey('challenges.id'), nullable=False),
        sa.Column("type", sa.String(length=80), nullable=True),
        sa.Column("location", sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'notifications',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('type', sa.Enum('TOAST', 'ALERT', 'BACKGROUND', default='TOAST', name='NotificationsType')),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )

    op.create_table(
        'awards',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('ctf_users.id'), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column('value', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.now()),
        sa.Column('updated_at', sa.DateTime(), default=datetime.now()),
    )


def downgrade() -> None:
    op.drop_table('campus')
    op.drop_table('ctf_users')
    op.drop_table('user_bans')
    op.drop_table('categories')
    op.drop_table('difficulties')
    op.drop_table('flags')
    op.drop_table('challenge_authors')
    op.drop_table('challenges')
    op.drop_table('submissions')
    op.drop_table('solves')
    op.drop_table('challenge_files')
    op.drop_table('notifications')
    op.drop_table('awards')
