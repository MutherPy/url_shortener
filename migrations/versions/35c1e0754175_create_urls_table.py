"""create urls table

Revision ID: 35c1e0754175
Revises: 
Create Date: 2026-11-11 17:50:04.641131
"""

from typing import Sequence, Union

from alembic import op


revision: str = '35c1e0754175'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE urls (
        code VARCHAR(9) PRIMARY KEY,
        original_url VARCHAR(2049),
        shortened_url VARCHAR(150)
    )
               """)
    op.execute("""
        CREATE SEQUENCE urls_id_seq
    AS BIGINT
    START WITH 1
    INCREMENT BY 1
    MINVALUE 1
    NO CYCLE;
    """)


def downgrade() -> None:
    # Write SQL here to reverse the changes made by upgrade().
    pass
