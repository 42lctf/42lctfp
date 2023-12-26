"""Init User

Revision ID: 9364b74e1516
Revises: 
Create Date: 2023-12-26 19:54:36.399240

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '9364b74e1516'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'ctf_user',
        sa.Column('id', sa.String, primary_key=True, nullable=False),
        sa.Column('nickname', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('score', sa.Integer, nullable=True),
        sa.Column('is_admin', sa.Boolean, nullable=True),
        sa.Column('created_at', sa.DateTime),
    )

    op.create_table(
        'category',
        sa.Column('id', sa.String, primary_key=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime),
    )

    op.create_table(
        'challenge',
        sa.Column('id', sa.String, primary_key=True, nullable=False),
        sa.Column('difficulty', postgresql.ENUM('baby', 'easy', 'medium', 'hard', 'insane', name='difficulty')),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('flag', sa.String, nullable=False),
        sa.Column('category_id', sa.String, sa.ForeignKey('category.id'), nullable=False),
        sa.Column('created_at', sa.DateTime),
    )

    op.create_table(
        'hint',
        sa.Column('id', sa.String, primary_key=True, nullable=False),
        sa.Column('challenge_id', sa.String, sa.ForeignKey('challenge.id'), nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('cost', sa.Integer, nullable=True),
        sa.Column('created_at', sa.DateTime),
    )

    op.create_table(
        'user_challenges',
        sa.Column('id', sa.String, primary_key=True, nullable=False),
        sa.Column('user_id', sa.String, sa.ForeignKey('ctf_user.id'), nullable=False),
        sa.Column('challenge_id', sa.String, sa.ForeignKey('challenge.id'), nullable=False),
        sa.Column('created_at', sa.DateTime),
    )

    op.create_table(
        'challenge_files',
        sa.Column('id', sa.String, primary_key=True, nullable=False),
        sa.Column('challenge_id', sa.String, sa.ForeignKey('challenge.id'), nullable=False),
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

