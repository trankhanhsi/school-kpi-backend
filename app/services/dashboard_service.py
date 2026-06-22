from app.services.task_service import TaskService
from app.services.kpi_service import KpiService

class DashboardService:

    @staticmethod
    def summary(db, user_id: int):
        tasks = TaskService.get_all_tasks(db)

        return {
            "total_tasks": len(tasks),
            "kpi_score": KpiService.calculate_total_score(
                db,
                user_id
            )
        }
