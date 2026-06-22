"""add senha employee

Revision ID: 4bbdc7f00121
Revises: ae1e4be27b90
Create Date: 2026-05-31 09:39:05.021350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4bbdc7f00121'
down_revision: Union[str, Sequence[str], None] = 'ae1e4be27b90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass
    

def downgrade() -> None:
    pass
   
    # ### end Alembic commands ###
