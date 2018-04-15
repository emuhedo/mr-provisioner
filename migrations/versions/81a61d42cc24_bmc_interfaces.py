"""bmc interfaces

Revision ID: 81a61d42cc24
Revises: 138919866e75
Create Date: 2018-04-15 11:28:47.789095

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger('alembic.env')

Session = sessionmaker()

# revision identifiers, used by Alembic.
revision = '81a61d42cc24'
down_revision = '138919866e75'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interface', sa.Column('bmc_id', sa.Integer(), nullable=True))
    op.alter_column('interface', 'mac',
               existing_type=postgresql.MACADDR(),
               nullable=True)
    op.create_foreign_key(None, 'interface', 'BMC', ['bmc_id'], ['id'], ondelete='CASCADE')

    session = Session(bind=bind)
    s = sa.sql.text('SELECT id, ip FROM \"BMC\"')
    result = session.execute(s)
    bmcs = result.fetchall()
    si = sa.sql.text('INSERT INTO interface(static_ipv4, bmc_id) VALUES(:static_ipv4, :bmc_id)')
    for bmc in bmcs:
        session.execute(si, {'static_ipv4': bmc['ip'], 'bmc_id': bmc['id']})
    session.commit()

    op.drop_constraint('BMC_ip_key', 'BMC', type_='unique')
    op.drop_column('BMC', 'ip')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'interface', type_='foreignkey')
    op.alter_column('interface', 'mac',
               existing_type=postgresql.MACADDR(),
               nullable=False)
    op.drop_column('interface', 'bmc_id')
    op.add_column('BMC', sa.Column('ip', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('BMC_ip_key', 'BMC', ['ip'])
    # ### end Alembic commands ###