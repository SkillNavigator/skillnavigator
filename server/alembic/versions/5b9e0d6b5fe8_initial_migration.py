"""Initial migration

Revision ID: 5b9e0d6b5fe8
Revises: 0b04a77e991f
Create Date: 2024-01-08 17:03:29.633056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b9e0d6b5fe8'
down_revision: Union[str, None] = '0b04a77e991f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('llm_answers', sa.Column('course_level', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('llm_answers', 'course_level')
    # ### end Alembic commands ###
