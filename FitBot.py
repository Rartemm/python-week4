# Libraries needed for the work.
import json
import telebot
from telebot import types

# Activating the bot.
bot = telebot.TeleBot("6582384996:AAGHGu8ix9kJKIfz9icC2QT34FHWUKik0UQ")

# Creating a shortcut for easier access of the files.
# Please adjust the path to your own computer!
# Files will be present in the repository
file_path_food = "C:\\Users\\Artem\\Downloads\\food_data.json"
file_path_work = "C:\\Users\\Artem\\Downloads\\workouts_data.json"

# Checking whether the user interacts with the bot for the first time
interacted_users = set()

# Tracked calories.
total_calories = 0

# List of commands.
commands = [
    "/start", 
    "/give_data", 
    "/cal_intake", 
    "/BMI",
    "/water_consumption",
    "/track_cals",
    "/add_food",
    "/reset_cals",
    "/show_cals",
    "/workouts"
    ]

# Dictionary for user's data.
user_data = {
    "Gender": None,
    "Age": None,
    "Height": None,
    "Weight": None,
    "Activity Level": None
}

# Activity level defenitions (used for calorie intake).
activity_level = {
    1: 1.2,
    2: 1.375,
    3: 1.55,
    4: 1.725,
    5: 1.9
}

# Activity level factor (used for water consumption).
activity_level_f = {
    1: 0.5,
    2: 0.6,
    3: 0.7,
    4: 0.8,
    5: 1.0
}

# Telling the user available commands.
@bot.message_handler(commands=["help"])
def help(message):
    commands_list = "\n".join(commands)
    bot.send_message(
        message.chat.id,
        f"Here is the list of available commands:\n{commands_list}")

# Greetings (task N.1).
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    
    if user_id not in interacted_users:
        # Add the user ID to the set of interacted users
        interacted_users.add(user_id)
        
        # Create a keyboard with a button to greet the user
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        greeting_button = types.KeyboardButton("👋 Greet me!")
        markup.add(greeting_button)
        
        bot.send_message(
            message.chat.id,
            "👋 Hello! I am your FitBot. I am here to assist you with your fitness journey.",
            reply_markup=markup
        )
    else:
        # If the user has already interacted, send a standard /start message
        bot.send_message(
            message.chat.id,
            "👋 Hello! I am your FitBot. I am here to assist you with your fitness journey."
        )

# Handle the greeting button
@bot.message_handler(func=lambda message: message.text == "👋 Greet me!")
def greet_user(message):
    bot.send_message(
        message.chat.id,
        "🎉 Welcome! I'm glad you're here. Let's start your fitness journey!"
    )

# Creating a command that will guide the user to enter their data (task N.2).
@bot.message_handler(commands=["give_data"])
def give_data(message):
    collect_data(message)

# Checking is the data was already entered and asking for it if not.
def collect_data(message):
    if user_data["Gender"] is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Male")
        btn2 = types.KeyboardButton("Female")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.chat.id,
                         "Please choose your gender",
                          reply_markup=markup)
        bot.register_next_step_handler(msg, process_gender)
    elif user_data["Age"] is None:
        bot.send_message(message.chat.id, "Please enter your age.")
        bot.register_next_step_handler(message, process_age)
    elif user_data["Height"] is None:
        bot.send_message(message.chat.id, "Please enter your height in cm.")
        bot.register_next_step_handler(message, process_height)
    elif user_data["Weight"] is None:
        bot.send_message(message.chat.id, "Please enter your weight in kg.")
        bot.register_next_step_handler(message, process_weight)
    elif user_data["Activity Level"] is None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btns = [types.KeyboardButton(str(i)) for i in range(1, 6)]
        markup.add(*btns)
        msg = bot.send_message(message.chat.id,
                         "Please choose your activity level (1-5)",
                          reply_markup=markup )
        bot.register_next_step_handler(msg, process_activity_level)
    else:
        bot.send_message(message.chat.id, "Thank you for providing your data!")

# Checking for a valid input (gender).
def process_gender(message):
    gender = message.text.lower()
    if gender == "male" or gender == "female":
        user_data["Gender"] = gender
        bot.send_message(
            message.chat.id, 
            f"You selected your gender: {gender}"
            )
        collect_data(message)
    else:
        bot.send_message(
            message.chat.id, 
            "Invalid input! Please enter Male or Female."
            )
        bot.register_next_step_handler(message, process_gender)

# Checking for a valid input (age).
def process_age(message):   
    age_input = message.text
    if age_input.isdigit():
        age = int(age_input)
        user_data["Age"] = age
        bot.send_message(
            message.chat.id, 
            f"Your entered age is {age} years."
            )
        collect_data(message)
    else:
        bot.send_message(
            message.chat.id, 
            "Invalid input! Please enter a valid number for age."
            )
        bot.register_next_step_handler(message, process_age)

# Checking for a valid input (height).
def process_height(message):
    height_input = message.text
    try:
        height = float(height_input)
        user_data["Height"] = height
        bot.send_message(
            message.chat.id, 
            f"Your entered height is {height} cm."
            )
        collect_data(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 
            "Invalid input! Please enter a valid integer for height."
            )
        bot.register_next_step_handler(message, process_height)

# Checking for a valid input (wight).
def process_weight(message):
    weight_input = message.text
    try:
        weight = float(weight_input)
        user_data["Weight"] = weight
        bot.send_message(
            message.chat.id, 
            f"Your entered weight is {weight} kg."
            )
        collect_data(message)
    except ValueError:
        bot.send_message(
            message.chat.id, 
            "Invalid input! Please enter a valid integer for weight."
            )
        bot.register_next_step_handler(message, process_weight)

# Checking for a valid input (activity level).
def process_activity_level(message):
    activity_level = message.text
    if activity_level.isdigit() and 1 <= int(activity_level) <= 5:
        user_data["Activity Level"] = int(activity_level)
        bot.send_message(
            message.chat.id, 
            f"Your selected activity level: {activity_level}"
            )
        collect_data(message)
    else:
        bot.send_message(
            message.chat.id, 
            "Invalid input! Please enter a number between 1 and 5 for activity level."
            )
        bot.register_next_step_handler(message, process_activity_level)

# Calculating user's daily calorie intake (task N.3).
@bot.message_handler(commands=["cal_intake"])
def cal_intake(message):
    missing_data = [key for key, value in user_data.items() if value is None]
        
    if missing_data:
        missing_fields = ", ".join(missing_data)
        bot.send_message(
            message.chat.id, 
            f"You're missing data for: {missing_fields}. Please complete your data first by entering a command /give_data."
            )
        return
        
    intake = 0

    if user_data["Gender"] == "male":
        intake = (10 * user_data["Weight"] 
                  + 6.25 * user_data["Height"] 
                  - 5 * user_data["Age"]
                  + 5) * activity_level[user_data["Activity Level"]]
    
    if user_data["Gender"] == "female":
        intake = (10 * user_data["Weight"]
                  + 6.25 * user_data["Height"]
                  - 5 * user_data["Age"]
                  + 161) * activity_level[user_data["Activity Level"]]
        
    bot.send_message(
        message.chat.id, 
        f"Your daily calorie intake is approximately {intake} calories"
        )

# Calculating user's BMI (task N.4).
@bot.message_handler(commands=["BMI"])
def BMI(message):        
    if user_data["Weight"] is None or user_data["Height"] is None:
        bot.send_message(
            message.chat.id, 
            f"You're missing data for weight or height. Please complete your data first by entering a command /give_data."
            )
        return
    
    bmi = user_data["Weight"] / (user_data["Height"] / 100) ** 2

    bot.send_message(
        message.chat.id, 
        f"Your Body Mass Index (BMI) is {bmi}"
        )

# Calculating water consumption (task N.5).
@bot.message_handler(commands=["water_consumption"])
def water_consumption(message):
    if user_data["Weight"] is None or user_data["Activity Level"] is None:
        bot.send_message(
            message.chat.id, 
            f"You're missing data for weight or activity level. Please complete your data first by entering a command /give_data."
            )
        return

    w_consumption = user_data["Weight"] * 2.20462 * activity_level_f[user_data["Activity Level"]]
    w_consumption_liters = w_consumption * 0.0295735

    bot.send_message(
        message.chat.id, 
        f"Your daily water cosumption should be {w_consumption} ounces or {w_consumption_liters} liters"
        )

# Downloading the list of foods.
def load_food_data():
    with open(file_path_food, 'r') as file:
        food_data = json.load(file)
    return food_data

# Tracking calories (task N.6).
@bot.message_handler(commands=["track_cals"])
def track_cals(message):
    bot.send_message(
        message.chat.id, 
        "Please, enter a food item that you want to track"
        )
    with open(file_path_food, 'r') as file:
        food_data = json.load(file)

    available_foods = "\n".join(
        [f"{item}: {calories} calories" for item, calories in food_data.items()]
        )
    
    bot.send_message(
        message.chat.id, 
        f"Here is the list of available food items:\n{available_foods}"
    )

    bot.register_next_step_handler(message, process_track_cals, food_data)

# Checking for a valid input.
def process_track_cals(message, food_data):
    global total_calories
    
    food_item = message.text.lower()

    if food_item in food_data:
        calorie_count = food_data[food_item]
        total_calories += calorie_count
        bot.send_message(
            message.chat.id,
            f"You've added {calorie_count}. Total calories: {total_calories}"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Sorry, the entered item is not available in the database. If you would like to add food, type /add_food."
        )

# Adding new food (key first) (task N.7).
@bot.message_handler(commands=["add_food"])
def add_food(message):
    bot.send_message(
        message.chat.id, 
        "Please enter the name of the new food item:"
        )
    bot.register_next_step_handler(message, process_new_food)

# Chechking for duplicates and prompting the user to enter the number of calories.
def process_new_food(message):
    new_food_name = message.text.lower()
    food_data = load_food_data()
    
    if new_food_name in food_data:
        bot.send_message(
            message.chat.id,
            f"The food item '{new_food_name}' is already present in the list."
        )
    else:
        bot.send_message(
            message.chat.id, 
            f"Please enter the calorie count for {new_food_name} (please enter whole numbers):"
            )
        bot.register_next_step_handler(message, process_new_calories, new_food_name)

# Checking for a valid response (to calories) and adding everything to the list.
def process_new_calories(message, new_food_name):
    new_calories_input = message.text
    if new_calories_input.isdigit():
        new_calories = int(new_calories_input)
        food_data = load_food_data()
        food_data[new_food_name] = new_calories
        with open(file_path_food, 'w') as file:
            json.dump(food_data, file, indent=4)
        bot.send_message(
            message.chat.id,
            f"New food item '{new_food_name}' with {new_calories} calories has been added."
        )
    else:
        bot.send_message(
            message.chat.id,
            "Invalid input! Please enter a valid number for calorie count."
        )

# Resetting calories (task N.8).
@bot.message_handler(commands=["reset_cals"])
def reset_cals(message):
    global total_calories

    total_calories = 0

    bot.send_message(
        message.chat.id,
        "You've successfully reset your caloriy count"
    )

# Displaying calories (task N.9).
@bot.message_handler(commands=["show_cals"])
def show_cals(message):
    global total_calories

    bot.send_message(
        message.chat.id, 
        f"Your tally of consumed calories is {total_calories} calories"
    )

# Downloading the list of workouts.
def load_workouts_data():
    with open(file_path_work, 'r') as file:
        workouts_data = json.load(file)
    return workouts_data

# Displaying workout options using buttons (task N.10).
@bot.message_handler(commands=["workouts"])
def workouts(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    available_calories = [50, 100, 200, 300, 400, 500, 1000]
    
    btns = [types.KeyboardButton(str(calories)) for calories in available_calories]
    markup.add(*btns)
    
    bot.send_message(
        message.chat.id, 
        "Please choose the number of calories you want to burn:",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, process_workout_calories)

# Checking for a valid response and providing the user with links.
def process_workout_calories(message):
    calories_input = message.text
    if calories_input.isdigit():
        calories_goal = int(calories_input)
        
        if user_data["Gender"] is None:
            bot.send_message(
                message.chat.id,
                "You haven't provided your gender. Please complete your data by entering the command /give_data."
            )
            return
        
        workouts_data = load_workouts_data()
        gender = user_data["Gender"]
        
        if gender in workouts_data:
            workout_options = workouts_data[gender]
            
            available_calories = [int(calories) for calories in workout_options.keys()]
            closest_calories = min(available_calories, key=lambda x: abs(x - calories_goal))
            
            workout_links = workout_options[str(closest_calories)]
            
            bot.send_message(
                message.chat.id,
                f"Here are some workout options to help you burn {closest_calories} calories:\n"
            )
            for link in workout_links:
                bot.send_message(message.chat.id, link)
        else:
            bot.send_message(
                message.chat.id,
                "Sorry, workout options are not available for your gender."
            )
    else:
        bot.send_message(
            message.chat.id,
            "Invalid input! Please choose a valid number of calories from the provided options."
        )
    calories_input = message.text

# Handling invalid inputs while texting.
@bot.message_handler()
def info(message):
    if message.text.lower() not in commands:
        bot.send_message(
            message.chat.id,
            "Sorry, I do not understand you. Type /help to see available commands"
        )

# Making sure the bot is always active, while the code is running
bot.polling(non_stop=True)