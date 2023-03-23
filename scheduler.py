from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor
import config


jobstores = {
    'default': RedisJobStore(jobs_key="notify_jobs", run_times_key="notify_running", host=config.REDIS_HOST, port=config.REDIS_PORT)
}


executors = {
    'default': AsyncIOExecutor(),
}

scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, timezone=timezone("Europe/Moscow"))
