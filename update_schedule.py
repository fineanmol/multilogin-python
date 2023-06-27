import json
from scheduler import update_schedule

def input_schedule():
    # Load the existing schedule from the file
    with open('config.json') as file:
        config = json.load(file)

    actions = {
        "1": {
            "action": "do_nothing",
            "parameters": {}
        },
        "2": {
            "action": "follow_accounts",
            "parameters": {}
        },
        "3": {
            "action": "like_posts",
            "parameters": {}
        },
        "4": {
            "action": "update_bio",
            "parameters": {}
        }
    }

    updated_config = {}

    for day, event in config.items():
        print(f"\nDay {day}:")
        print("Available actions:")
        print("1. Do nothing")
        print("2. Follow people")
        print("3. Like posts")
        print("4. Update bio")

        choices = input("Choose the actions for this day (comma-separated): ").split(',')

        day_actions = []
        for choice in choices:
            while choice not in actions:
                print("Invalid choice. Please choose a valid action.")
                choice = input("Choose the actions for this day (comma-separated): ")

            if choice == "2":
                follow_count = input("Enter the number of accounts to follow: ")
                while not follow_count.isdigit():
                    print("Invalid input. Please enter a valid number.")
                    follow_count = input("Enter the number of accounts to follow: ")
                actions[choice]["parameters"]["follow_count"] = int(follow_count)
            elif choice == "3":
                like_count = input("Enter the number of posts to like: ")
                while not like_count.isdigit():
                    print("Invalid input. Please enter a valid number.")
                    like_count = input("Enter the number of posts to like: ")
                actions[choice]["parameters"]["like_count"] = int(like_count)
                
            day_actions.append(actions[choice])

        if day_actions:
            updated_config[day] = day_actions
        else:
            print("Invalid choices. Skipping this day.")
            continue

    # Update the schedule file with the new configuration
    with open('config.json', 'w') as file:
        json.dump(updated_config, file)

    print("Schedule updated successfully.")

# Usage example
input_schedule()
with open('config.json') as file:
    config = json.load(file)
update_schedule(config)
