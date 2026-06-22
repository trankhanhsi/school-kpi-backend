from app.models.base import Base
from app.models.school import School
from app.models.role import Role
from app.models.department import Department
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.refresh_token import RefreshToken
from app.models.task import Task
from app.models.evidence import Evidence
from app.models.kpi_rule import KpiRule
from app.models.kpi_event import KPIEvent
from app.models.kpi_summary_monthly import KPISummaryMonthly
from app.models.kpi_summary_semester import KpiSummarySemester
from app.models.kpi_summary_yearly import KpiSummaryYearly
from app.models.notification import Notification
from app.models.audit_log import AuditLog

# Xuất bản (Export) tất cả các thực thể để SQLAlchemy ánh xạ đúng vị trí
__all__ = [
    "Base", "School", "Role", "Department", "User", "UserProfile", 
    "RefreshToken", "Task", "Evidence", "KpiRule", "KPIEvent", 
    "KPISummaryMonthly", "KpiSummarySemester", "KpiSummaryYearly", 
    "Notification", "AuditLog"
]