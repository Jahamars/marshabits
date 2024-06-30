import os
import json
import datetime
import urwid

# Directories to store habits and deleted habits in JSON format
HABITS_DIR = 'habits_json'
TRASH_DIR = 'trash_bin'

# Create the directories if they don't exist
if not os.path.exists(HABITS_DIR):
    os.makedirs(HABITS_DIR)
if not os.path.exists(TRASH_DIR):
    os.makedirs(TRASH_DIR)

# Function to load habits from the JSON files
def load_habits(directory):
    habits = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            habit_name = filename[:-5]
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                habits[habit_name] = data
    return habits

# Function to save a habit to a JSON file
def save_habit(habit_name, details, directory):
    with open(os.path.join(directory, f'{habit_name}.json'), 'w') as file:
        json.dump(details, file, indent=4)

# Function to delete a habit
def delete_habit(habits, habit_name):
    if habit_name in habits:
        # Move habit to trash bin
        save_habit(habit_name, habits[habit_name], TRASH_DIR)
        del habits[habit_name]
        os.remove(os.path.join(HABITS_DIR, f'{habit_name}.json'))
        update_ui()

# Function to add or edit a habit
def add_or_edit_habit(habits, habit_name=None):
    if habit_name:
        habit_data = habits[habit_name]
    else:
        habit_data = {'description': '', 'dates': []}

    def save_new_habit(button):
        new_habit_name = edit_name.get_edit_text()
        description = edit_description.get_edit_text()
        habits[new_habit_name] = {'description': description, 'dates': habit_data['dates']}
        save_habit(new_habit_name, habits[new_habit_name], HABITS_DIR)
        update_ui()

    edit_name = urwid.Edit("Enter the name of the habit: ", habit_name or "")
    edit_description = urwid.Edit("Enter the description of the habit:\n", habit_data['description'], multiline=True)
    button_save = urwid.Button("Save", save_new_habit)
    back_button = urwid.Button("Back", lambda button: update_ui())
    pile = urwid.Pile([edit_name, edit_description, button_save, back_button])
    fill = urwid.Filler(pile)
    loop.widget = urwid.Padding(fill, left=2, right=2)

# Function to display habits
def display_habits(habits):
    today = datetime.date.today().strftime('%Y-%m-%d')
    habit_names = sorted(habits.keys())
    
    def show_habit_details(button, habit_name):
        details = habits[habit_name]
        text = [f"Habit: {habit_name}\n", f"Description: {details['description']}\n", "Dates:\n"]
        for date in details['dates']:
            text.append(f"  {date}\n")
        back_button = urwid.Button("Back", lambda button: update_ui())
        delete_button = urwid.Button("Delete", lambda button: delete_habit(habits, habit_name))
        edit_button = urwid.Button("Edit", lambda button: add_or_edit_habit(habits, habit_name))
        pile = urwid.Pile([urwid.Text(''.join(text)), back_button, edit_button, delete_button])
        fill = urwid.Filler(pile)
        loop.widget = urwid.Padding(fill, left=2, right=2)
    
    buttons = []
    for habit_name in habit_names:
        status = "[X]" if today in habits[habit_name]['dates'] else "[ ]"
        button = urwid.Button(f"{status} {habit_name}", lambda button, name=habit_name: show_habit_details(button, name))
        buttons.append(button)
    back_button = urwid.Button("Back", lambda button: update_ui())
    pile = urwid.Pile(buttons + [back_button])
    fill = urwid.Filler(pile)
    loop.widget = urwid.Padding(fill, left=2, right=2)

# Function to plot habits
def plot_habits(habits):
    def show_statistics(button, stat_type):
        habits = load_habits(HABITS_DIR)
        stats_text = []
    
        if stat_type == 'all_time':
            stats_text.append("Statistics for all time:\n")
            for habit_name, habit in habits.items():
                stats_text.append(f"Habit: {habit_name}\n")
                stats_text.append(f"Description: {habit['description']}\n")
                stats_text.append("Dates:\n")
                for date in habit['dates']:
                    stats_text.append(f"  {date}\n")
                stats_text.append("\n")
    
        stats_display = urwid.Text(''.join(stats_text))
        back_button = urwid.Button("Back", lambda button: update_ui())
        pile = urwid.Pile([stats_display, back_button])
        fill = urwid.Filler(pile)
        loop.widget = urwid.Padding(fill, left=2, right=2)
    
    buttons = [
        urwid.Button("Last 10 days", lambda button: show_statistics(button, '10_days')),
        urwid.Button("Last month", lambda button: show_statistics(button, 'month')),
        urwid.Button("All time", lambda button: show_statistics(button, 'all_time')),
        urwid.Button("Back", lambda button: update_ui())
    ]
    pile = urwid.Pile(buttons)
    fill = urwid.Filler(pile)
    loop.widget = urwid.Padding(fill, left=2, right=2)

# Function to mark habits as done
def mark_habits_menu(habits):
    today = datetime.date.today().strftime('%Y-%m-%d')
    habit_buttons = []
    for habit_name, details in sorted(habits.items()):
        status = "[X]" if today in details['dates'] else "[ ]"
        habit_button = urwid.Button(f"{status} {habit_name}\nDescription: {details['description']}",
                                    lambda button, name=habit_name: mark_habit_done(habits, name))
        habit_buttons.append(habit_button)
    
    back_button = urwid.Button("Back", lambda button: update_ui())
    pile = urwid.Pile(habit_buttons + [back_button])
    fill = urwid.Filler(pile)
    loop.widget = urwid.Padding(fill, left=2, right=2)

# Main menu function
def main_menu():
    habits = load_habits(HABITS_DIR)
    main_menu_text = urwid.Text("""
┳┳┓       ┓┏  ┓ •  
┃┃┃┏┓┏┓┏━━┣┫┏┓┣┓┓╋┏
┛ ┗┗┻┛ ┛  ┛┗┗┻┗┛┗┗┛
                                                                          
\n""")
    
    buttons = [
        urwid.Button("1. Add a new habit", lambda button: add_or_edit_habit(habits)),
        urwid.Button("2. Display habits", lambda button: display_habits(habits)),
        urwid.Button("3. Plot habits", lambda button: plot_habits(habits)),
        urwid.Button("4. Mark habits as done", lambda button: mark_habits_menu(habits)),
        urwid.Button("5. Delete a habit", lambda button: delete_habit_menu(habits)),
        urwid.Button("6. Manage Trash Bin", lambda button: manage_trash_bin()),
        urwid.Button("7. Quit", lambda button: exit_program())
    ]
    
    pile = urwid.Pile([main_menu_text] + buttons)
    fill = urwid.Filler(pile)
    return urwid.Padding(fill, left=2, right=2)

# Function to display the list of today's habits
def habit_list(habits):
    today = datetime.date.today().strftime('%Y-%m-%d')
    buttons = []
    for habit_name, details in sorted(habits.items()):
        status = "[X]" if today in details['dates'] else "[ ]"
        button = urwid.Text(f"{status} {habit_name}")
        buttons.append(button)
    return urwid.Pile(buttons)

# Function to display the 10-day progress
def ten_day_progress(habits):
    today = datetime.date.today()
    last_10_days = [today - datetime.timedelta(days=i) for i in range(10)]
    text = ["Progress for the last 10 days:\n"]
    for day in last_10_days[::-1]:
        day_str = day.strftime('%Y-%m-%d')
        completed = sum(1 for habit in habits.values() if day_str in habit['dates'])
        percentage = (completed / len(habits)) * 100 if habits else 0
        text.append(f"{day_str}: {'#' * int(percentage // 10)}{' ' * (10 - int(percentage // 10))} ({percentage:.0f}%)\n")
    return urwid.Text(''.join(text))

# Function to update the UI
def update_ui():
    habits = load_habits(HABITS_DIR)
    left_column = urwid.LineBox(main_menu())
    middle_column = urwid.LineBox(habit_list(habits))
    right_column = urwid.LineBox(ten_day_progress(habits))
    columns = urwid.Columns([('weight', 2, left_column), ('weight', 1, middle_column), ('weight', 1, right_column)])
    fill = urwid.Filler(columns)
    loop.widget = fill

# Function to handle keyboard shortcuts
def handle_shortcuts(key):
    if key in ('1', 'a'):
        add_or_edit_habit(load_habits(HABITS_DIR))
    elif key in ('2', 'd'):
        display_habits(load_habits(HABITS_DIR))
    elif key in ('3', 'p'):
        plot_habits(load_habits(HABITS_DIR))
    elif key in ('4', 'm'):
        mark_habits_menu(load_habits(HABITS_DIR))
    elif key in ('5', 'x'):
        delete_habit_menu(load_habits(HABITS_DIR))
    elif key in ('6', 't'):
        manage_trash_bin()
    elif key in ('7', 'q', 'Q'):
        exit_program()
    elif key == 'b':
        update_ui()

# Function to delete a habit menu
def delete_habit_menu(habits):
    habit_buttons = []
    for habit_name in sorted(habits.keys()):
        habit_button = urwid.Button(f"Delete {habit_name}",
                                    lambda button, name=habit_name: confirm_delete_habit(habits, name))
        habit_buttons.append(habit_button)
    
    back_button = urwid.Button("Back", lambda button: update_ui())
    pile = urwid.Pile(habit_buttons + [back_button])
    fill = urwid.Filler(pile)
    loop.widget = urwid.Padding(fill, left=2, right=2)

def confirm_delete_habit(habits, habit_name):
    def delete_confirmed(button):
        delete_habit(habits, habit_name)
        update_ui()

    text = urwid.Text([f"Are you sure you want to delete the habit '{habit_name}'?\n"])
    button_yes = urwid.Button("Yes", delete_confirmed)
    button_no = urwid.Button("No", lambda button: delete_habit_menu(habits))
    pile = urwid.Pile([text, button_yes, button_no])
    fill = urwid.Filler(pile)
    loop.widget = urwid.Padding(fill, left=2, right=2)

def mark_habit_done(habits, habit_name):
    today = datetime.date.today().strftime('%Y-%m-%d')
    if today in habits[habit_name]['dates']:
        habits[habit_name]['dates'].remove(today)
    else:
        habits[habit_name]['dates'].append(today)
    save_habit(habit_name, habits[habit_name], HABITS_DIR)
    update_ui()

# Function to manage trash bin
def manage_trash_bin():
    trash_habits = load_habits(TRASH_DIR)

    def show_trash_habit_details(button, habit_name):
        details = trash_habits[habit_name]
        text = [f"Habit: {habit_name}\n", f"Description: {details['description']}\n", "Dates:\n"]
        for date in details['dates']:
            text.append(f"  {date}\n")
        back_button = urwid.Button("Back", lambda button: manage_trash_bin())
        restore_button = urwid.Button("Restore", lambda button: restore_habit(habit_name))
        delete_button = urwid.Button("Permanently Delete", lambda button: permanently_delete_habit(habit_name))
        pile = urwid.Pile([urwid.Text(''.join(text)), back_button, restore_button, delete_button])
        fill = urwid.Filler(pile)
        loop.widget = urwid.Padding(fill, left=2, right=2)

    def restore_habit(habit_name):
        habit_data = trash_habits.pop(habit_name)
        save_habit(habit_name, habit_data, HABITS_DIR)
        os.remove(os.path.join(TRASH_DIR, f'{habit_name}.json'))
        manage_trash_bin()

    def permanently_delete_habit(habit_name):
        trash_habits.pop(habit_name)
        os.remove(os.path.join(TRASH_DIR, f'{habit_name}.json'))
        manage_trash_bin()

    buttons = []
    for habit_name in sorted(trash_habits.keys()):
        button = urwid.Button(f"{habit_name}", lambda button, name=habit_name: show_trash_habit_details(button, name))
        buttons.append(button)
    back_button = urwid.Button("Back", lambda button: update_ui())
    pile = urwid.Pile(buttons + [back_button])
    fill = urwid.Filler(pile)
    loop.widget = urwid.Padding(fill, left=2, right=2)

# Function to exit the program
def exit_program():
    raise urwid.ExitMainLoop()

# Load habits and start the main loop
loop = urwid.MainLoop(urwid.SolidFill(), unhandled_input=handle_shortcuts)
try:
    update_ui()
    loop.run()
except KeyboardInterrupt:
    print("Программа завершена пользователем.")
