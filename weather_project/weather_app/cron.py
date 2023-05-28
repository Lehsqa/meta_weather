from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .utils import update_weather

scheduler = BackgroundScheduler()


def start():
    # Регистрируем задачу обновления погоды
    scheduler.add_job(update_weather, CronTrigger.from_crontab('0 9 * * *'))
    scheduler.start()


def reschedule(new_time: str):
    # Отмена текущего расписания обновления погоды
    scheduler.remove_all_jobs()

    # Парсинг нового времени обновления
    hour, minute = map(int, new_time.split(':'))

    # Назначение нового расписания обновления погоды
    scheduler.add_job(update_weather, 'cron', hour=hour, minute=minute)
