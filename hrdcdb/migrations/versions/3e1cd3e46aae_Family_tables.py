"""Family tables

Revision ID: 3e1cd3e46aae
Revises: 3654c268fc5e
Create Date: 2020-01-29 17:15:03.282709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e1cd3e46aae'
down_revision = '3654c268fc5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('case_note', sa.String(length=300), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_family_created_date'), 'family', ['created_date'], unique=False)
    op.create_table('family_member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('head_of_household', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('service')
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_type_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.Column('program_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('is_family', sa.Boolean(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    sa.ForeignKeyConstraint(['service_type_id'], ['service_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('service_type')
    op.create_table('service_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('units', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_service_created_date'), 'service', ['created_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('service')
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_type_id', sa.Integer(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=True),
    sa.Column('program_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('begin_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
    sa.ForeignKeyConstraint(['service_type_id'], ['service_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_table('service_type')
    op.create_table('service_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_service_created_date'), 'service', ['created_date'], unique=False)
    op.drop_table('family_member')
    op.drop_index(op.f('ix_family_created_date'), table_name='family')
    op.drop_table('family')
    # ### end Alembic commands ###