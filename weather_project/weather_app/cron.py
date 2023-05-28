from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .utils import update_weather

scheduler = BackgroundScheduler()


def start():
    # Register a weather update task
    scheduler.add_job(update_weather, CronTrigger.from_crontab('0 9 * * *'))
    scheduler.start()


def reschedule(new_time: str):
    # Cancelling the current weather update schedule
    scheduler.remove_all_jobs()

    # Parsing new update times
    hour, minute = map(int, new_time.split(':'))

    # Assigning a new weather update schedule
    scheduler.add_job(update_weather, 'cron', hour=hour, minute=minute)
