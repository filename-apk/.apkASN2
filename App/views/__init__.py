# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .StudentView import student_views
from .StaffView import staff_views
from .EmployerView import employer_views


views = [user_views, index_views, auth_views, student_views, staff_views, employer_views]
# blueprints must be added to this list