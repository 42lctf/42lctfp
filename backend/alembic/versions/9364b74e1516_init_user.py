"""Init User

Revision ID: 9364b74e1516
Revises: 
Create Date: 2023-12-26 19:54:36.399240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '9364b74e1516'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'ctf_user',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password', sa.String(50), nullable=True),
        sa.Column('campus_id', sa.BigInteger, nullable=True),
        sa.Column('intra_id', sa.BigInteger, nullable=True),
        sa.Column('nickname', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.String(150), nullable=True),
        sa.Column('website', sa.String(50), nullable=True),
        sa.Column('score', sa.Integer, default=0, nullable=True),
        sa.Column('is_admin', sa.Boolean, default=False, nullable=False),
        sa.Column('is_hidden', sa.Boolean, default=False, nullable=False),
        sa.Column('is_verified', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )

    op.create_table(
        'category',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

    op.create_table(
        'difficulty',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('level', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

    op.create_table(
        'flags',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('flag', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

    op.create_table(
        'parent_challenge',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('challenge_id', UUID, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

    op.create_table(
        'author',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('challenge_id', UUID, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

    op.create_table(
        'challenge',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=250), nullable=False),
        sa.Column('is_hidden', sa.Boolean, default=False, nullable=False),
        sa.Column('difficulty_id', UUID, sa.ForeignKey('difficulty.id'), nullable=False),
        sa.Column('flag_id', UUID, sa.ForeignKey('flags.id'), nullable=False),
        sa.Column('parent_id', UUID, sa.ForeignKey('parent_challenge.id'), nullable=False),
        sa.Column('category_id', UUID, sa.ForeignKey('category.id'), nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

    op.create_table(
        'user_challenges',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID, sa.ForeignKey('ctf_user.id'), nullable=False),
        sa.Column('challenge_id', UUID, sa.ForeignKey('challenge.id'), nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )

    op.create_table(
        'challenge_files',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('challenge_id', UUID, sa.ForeignKey('challenge.id'), nullable=False),
        sa.Column('created_at', sa.DateTime),
        # sa.Column('file_content', sa.String, sa.LargeBinary),
    )


def downgrade() -> None:
    op.drop_table('ctf_user')
    op.drop_table('category')
    op.drop_table('challenge')
    op.drop_table('hint')
    op.drop_table('user_challenges')
    op.drop_table('challenge_files')
