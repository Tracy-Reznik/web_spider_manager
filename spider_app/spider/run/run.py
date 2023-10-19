import threading
from spider_app.spider.task import video_task


def run_video_task(functionname, config: dict):
    task_function = globals().get(f"video_task.{functionname}")
    if task_function:
        thread = threading.Thread(task_function, args=config)
        thread.start()
