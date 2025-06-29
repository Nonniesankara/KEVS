"""Allow candidates for all positions

Revision ID: c6200e2143e2
Revises: 2469fba248e3
Create Date: 2025-06-28 21:46:51.075462
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c6200e2143e2'
down_revision = '2469fba248e3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('candidates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('constituency_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('county_id', sa.Integer(), nullable=True))
        batch_op.alter_column('ward_id',
                              existing_type=sa.INTEGER(),
                              nullable=True)

        # ✅ Add named foreign keys to avoid ValueError
        batch_op.create_foreign_key(
            'fk_candidates_county_id',
            'counties',
            ['county_id'],
            ['id']
        )
        batch_op.create_foreign_key(
            'fk_candidates_constituency_id',
            'constituencies',
            ['constituency_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('candidates', schema=None) as batch_op:
        # ✅ Use the exact constraint names to drop them
        batch_op.drop_constraint('fk_candidates_constituency_id', type_='foreignkey')
        batch_op.drop_constraint('fk_candidates_county_id', type_='foreignkey')
        batch_op.alter_column('ward_id',
                              existing_type=sa.INTEGER(),
                              nullable=False)
        batch_op.drop_column('county_id')
        batch_op.drop_column('constituency_id')
