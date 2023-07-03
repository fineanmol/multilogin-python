import concurrent.futures
import datetime
import logging
import random
import schedule
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - Thread %(thread)d - %(message)s')

warmup_configuration = [
        {
            "day_of_week": "Monday",
            "actions": [
                {
                    "action_type": "LIKE",
                    "sessions": [
                        {
                            "session_id": "session1",
                            "count": 2,
                            "start_time": "15:40:30",
                            "end_time": "20:00:00"
                        },
                        {
                            "session_id": "session2",
                            "count": 6,
                            "start_time": "15:42:30",
                            "end_time": "20:00:00"
                        },
                        {
                            "session_id": "session3",
                            "count": 27,
                            "start_time": "15:45:30",
                            "end_time": "20:00:00"
                        }
                    ]
                },
                {
                    "action_type": "FOLLOW",
                    "sessions": [
                        {
                            "session_id": "session1",
                            "count": 7,
                            "start_time": "15:40:30",
                            "end_time": "20:00:00"
                        },
                        {
                            "session_id": "session2",
                            "count": 23,
                            "start_time": "15:50:30",
                            "end_time": "20:00:00"
                        }
                    ]
                }
            ]
        }
    ]

profiles = ['profile1', 'profile2', 'profile3']

async def perform_action(profile_name, action_type, count, session_id,bot):
    # Create a Selenium WebDriver instance for the profile

    # Perform the action multiple times
    for i in range(count):
        # Generate a random delay between 0.5 and 1 second for each action
        action_delay = random.uniform(0.5, 1)
        time.sleep(action_delay)

        # Perform the action using Selenium commands
        if action_type == 'LIKE':
            logging.info(f"[Profile: {profile_name}] Session: {session_id} - [{action_type}] Like {i+1}/{count}")
            bot.instagram_like_posts(count)
            # Perform like action using Selenium
        elif action_type == 'FOLLOW':
            logging.info(f"[Profile: {profile_name}] Session: {session_id} - [{action_type}] Follow {i+1}/{count}")
            bot.instagram_follow_accounts()
            # Perform follow action using Selenium


    # Close the WebDriver

async def schedule_task(profile_name, action_type, count, session_id,bot):
    # Run the task immediately
    perform_action(profile_name, action_type, count, session_id,bot)

async def schedule_and_execute_tasks(bot):
    # Get the current weekday
    current_day = datetime.datetime.now().strftime("%A")

    # Retrieve the actions and their configurations for the current weekday from the warmup configuration
    actions = None
    for config in warmup_configuration:
        if config['day_of_week'] == current_day:
            actions = config['actions']
            break

    if not actions:
        logging.info(f"No action scheduled for {current_day}")
        return

    # Create a thread pool executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(profiles) * len(actions))

    # Schedule the tasks for each profile and action
    for profile_name in profiles:
        for action in actions:
            action_type = action['action_type']
            sessions = action['sessions']

            for session in sessions:
                session_id = session['session_id']
                count = session['count']
                start_time = session['start_time']
                end_time = session['end_time']

                # Schedule the task at the start time using the schedule library
                # schedule.every().day.at(start_time).do(executor.submit, schedule_task, profile_name, action_type, count, session_id,bot)
                logging.info(f"Scheduled task for [Profile: {profile_name}] Session: {session_id} - [{action_type}]")
    await bot.instagram_like_posts(count)

    # Run the schedule in a separate thread
    async def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Start the schedule thread
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)
