import asyncio
import concurrent.futures
import datetime
import random
import schedule
import threading
import time

from httpClient import HttpClient
from logger import Logger
from model.account import ActionType

# Configure logging
logger = Logger.get_instance()


def perform_action(profile_name, action_type, count, session_id):
    # Perform the action delay times
    action_delay = random.uniform(0.5, 1)
    time.sleep(action_delay)

    # Perform the action
    if action_type == ActionType.LIKE:
        logger.info(f"[Profile: {profile_name}] Session: {session_id} - [{action_type}] Like {1}/{count}")
    elif action_type == ActionType.FOLLOW:
        logger.info(f"[Profile: {profile_name}] Session: {session_id} - [{action_type}] Follow {1}/{count}")
    elif action_type == ActionType.BIO_UPDATE:
        logger.info(f"[Profile: {profile_name}] Session: {session_id} - [{action_type}] Bio Update {1}/{count}")
    elif action_type == ActionType.MEDIA_UPLOAD:
        logger.info(f"[Profile: {profile_name}] Session: {session_id} - [{action_type}] Media Upload {1}/{count}")
    elif action_type == ActionType.BLOCK:
        logger.info(f"[Profile: {profile_name}] Session: {session_id} - [{action_type}] Block {1}/{count}")


def schedule_task(profile_name, action_type, count, session_id):
    # Run the task immediately
    perform_action(profile_name, action_type, count, session_id)


def schedule_and_execute_tasks(profiles):
    # Get the current weekday
    current_day = datetime.datetime.now().strftime("%A")

    # Retrieve the actions and their configurations for the current weekday from the warmup configuration
    actions = None
    for profile in profiles:
        for account in profile['accounts']:
            for config in account['warmup_configuration']:
                if config['day_of_week'] == current_day:
                    actions = config['actions']
                    break
            if actions:
                break
        if actions:
            break

    if not actions:
        logger.info(f"No action scheduled for {current_day}")
        return

    # Create a thread pool executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(profiles) * len(actions))

    # Schedule the tasks for each profile, account, and action
    for profile in profiles:
        for account in profile['accounts']:
            profile_name = profile['uuid']
            for action in actions:
                action_type = action['action_type']
                sessions = action['sessions']

                for session in sessions:
                    session_id = session['session_id']
                    count = session['count']
                    start_time = session['start_time']
                    end_time = session['end_time']

                    # Schedule the task at the start time using the schedule library
                    schedule.every().day.at(start_time).do(executor.submit, schedule_task,
                                                           profile_name, action_type, count, session_id)
                    logger.info(f"Scheduled task for [Profile: {profile_name}] Session: {session_id} - [{action_type}]")

    # Run the schedule in a separate thread
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Start the schedule thread
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)


async def main():
    profiles = await HttpClient("http://127.0.0.1:3001/profile") \
        .get("/warmup/list")

    schedule_and_execute_tasks(profiles)

# Example usage
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())