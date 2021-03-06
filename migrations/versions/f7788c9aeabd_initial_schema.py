"""initial schema

Revision ID: f7788c9aeabd
Revises: 
Create Date: 2021-05-03 12:22:04.333865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7788c9aeabd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('street', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=80), nullable=True),
    sa.Column('zipcode', sa.String(length=30), nullable=True),
    sa.Column('state', sa.String(length=30), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('address_id')
    )
    op.create_table('qualificationdate',
    sa.Column('priority_group', sa.Integer(), nullable=False),
    sa.Column('qualify_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('priority_group')
    )
    op.create_table('timeblockoptions',
    sa.Column('time_block_id', sa.Integer(), nullable=False),
    sa.Column('time_block_start', sa.Time(), nullable=False),
    sa.Column('time_block_end', sa.Time(), nullable=False),
    sa.Column('day_of_week', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('time_block_id')
    )
    op.create_table('userlogin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_type', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_userlogin_username'), 'userlogin', ['username'], unique=True)
    op.create_table('patient',
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('patient_name', sa.String(length=80), nullable=True),
    sa.Column('ssn', sa.String(length=11), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=True),
    sa.Column('priority_group', sa.Integer(), nullable=True),
    sa.Column('login_id', sa.Integer(), nullable=True),
    sa.Column('max_distance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.address_id'], ),
    sa.ForeignKeyConstraint(['login_id'], ['userlogin.id'], ),
    sa.ForeignKeyConstraint(['priority_group'], ['qualificationdate.priority_group'], ),
    sa.PrimaryKeyConstraint('patient_id')
    )
    op.create_table('provider',
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('provider_name', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=True),
    sa.Column('provider_type', sa.String(length=80), nullable=True),
    sa.Column('login_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.address_id'], ),
    sa.ForeignKeyConstraint(['login_id'], ['userlogin.id'], ),
    sa.PrimaryKeyConstraint('provider_id')
    )
    op.create_table('appointment',
    sa.Column('appointment_id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('appointment_time', sa.DateTime(), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.provider_id'], ),
    sa.PrimaryKeyConstraint('appointment_id')
    )
    op.create_index(op.f('ix_appointment_appointment_time'), 'appointment', ['appointment_time'], unique=False)
    op.create_table('timepreference',
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('time_block_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.ForeignKeyConstraint(['time_block_id'], ['timeblockoptions.time_block_id'], )
    )
    op.create_table('appointmentmatch',
    sa.Column('match_id', sa.Integer(), nullable=False),
    sa.Column('appointment_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('offer_status', sa.String(length=20), nullable=True),
    sa.Column('time_offer_made', sa.DateTime(), nullable=True),
    sa.Column('time_offer_expires', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['appointment_id'], ['appointment.appointment_id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('match_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appointmentmatch')
    op.drop_table('timepreference')
    op.drop_index(op.f('ix_appointment_appointment_time'), table_name='appointment')
    op.drop_table('appointment')
    op.drop_table('provider')
    op.drop_table('patient')
    op.drop_index(op.f('ix_userlogin_username'), table_name='userlogin')
    op.drop_table('userlogin')
    op.drop_table('timeblockoptions')
    op.drop_table('qualificationdate')
    op.drop_table('address')
    # ### end Alembic commands ###
