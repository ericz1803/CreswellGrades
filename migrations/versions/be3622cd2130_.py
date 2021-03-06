"""empty message

Revision ID: be3622cd2130
Revises: 3ffa5f8f05af
Create Date: 2019-08-18 18:41:49.289947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be3622cd2130'
down_revision = '3ffa5f8f05af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('assignment_class_id_fkey', 'assignment', type_='foreignkey')
    op.create_foreign_key(None, 'assignment', 'class', ['class_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('assignmentresult_assignment_id_fkey', 'assignmentresult', type_='foreignkey')
    op.create_foreign_key(None, 'assignmentresult', 'assignment', ['assignment_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('classstdentlink_student_id_fkey', 'classstdentlink', type_='foreignkey')
    op.drop_constraint('classstdentlink_class_id_fkey', 'classstdentlink', type_='foreignkey')
    op.create_foreign_key(None, 'classstdentlink', 'users', ['student_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'classstdentlink', 'class', ['class_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('gradefactor_class_id_fkey', 'gradefactor', type_='foreignkey')
    op.create_foreign_key(None, 'gradefactor', 'class', ['class_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('gradescale_class_id_fkey', 'gradescale', type_='foreignkey')
    op.create_foreign_key(None, 'gradescale', 'class', ['class_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'gradescale', type_='foreignkey')
    op.create_foreign_key('gradescale_class_id_fkey', 'gradescale', 'class', ['class_id'], ['id'])
    op.drop_constraint(None, 'gradefactor', type_='foreignkey')
    op.create_foreign_key('gradefactor_class_id_fkey', 'gradefactor', 'class', ['class_id'], ['id'])
    op.drop_constraint(None, 'classstdentlink', type_='foreignkey')
    op.drop_constraint(None, 'classstdentlink', type_='foreignkey')
    op.create_foreign_key('classstdentlink_class_id_fkey', 'classstdentlink', 'class', ['class_id'], ['id'])
    op.create_foreign_key('classstdentlink_student_id_fkey', 'classstdentlink', 'users', ['student_id'], ['id'])
    op.drop_constraint(None, 'assignmentresult', type_='foreignkey')
    op.create_foreign_key('assignmentresult_assignment_id_fkey', 'assignmentresult', 'assignment', ['assignment_id'], ['id'])
    op.drop_constraint(None, 'assignment', type_='foreignkey')
    op.create_foreign_key('assignment_class_id_fkey', 'assignment', 'class', ['class_id'], ['id'])
    # ### end Alembic commands ###
