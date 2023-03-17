import telegram
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, CallbackQueryHandler
import queue
import random
import asyncio


# Define the function for handling the /start command
# def start(update, context):
def start(update: Update, context: CallbackContext) -> None:
    # Create an inline keyboard with language options
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data="en"),
            InlineKeyboardButton("Українська 🇺🇦", callback_data="uk"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the welcome message and inline keyboard to the user
    update.message.reply_text(
        "Welcome to my bot! Please select a language:",
        reply_markup=reply_markup
    )

    chat_id = update.effective_chat.id
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Welcome to my bot.")
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Hello, I'm your sandwich bot! Use the /sandwich command to generate a random sandwich.")
    # context.bot.send_message(chat_id=chat_id, text=greeting, parse_mode=telegram.ParseMode.HTML)


def language_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    language = query.data

    # Store the user's language preference in the user data
    context.user_data["language"] = language

    # Send a confirmation message to the user
    if language == "en":
        message = "Language set to English 🇬🇧"
    elif language == "uk":
        message = "Мову встановлено на українську 🇺🇦"
    query.answer(message)


# Define the ingredients for each type
bread_types = ["white bread", "whole wheat bread", "rye bread", "baguette", "ciabatta", "sourdough bread", "pita bread",
               "multigrain bread", "focaccia", "brioche", "croissant", "naan", "tortilla", "lavash", "panini", "bagel",
               "english muffin", "cinnamon raisin bread", "pumpernickel bread", "cornbread"]
meat_types = ["turkey", "ham", "roast beef", "chicken", "bacon", "salami", "pastrami", "corned beef", "pepperoni",
              "prosciutto", "meatballs", "sausage", "pulled pork", "beef brisket", "chorizo", "lamb", "venison", "duck",
              "pork belly", "veal"]
cheese_types = ["cheddar", "swiss", "mozzarella", "provolone", "american", "brie", "goat cheese", "blue cheese", "feta",
                "pepper jack", "gouda", "monterey jack", "ricotta", "parmesan", "asiago", "colby jack", "manchego",
                "havarti", "queso blanco", "smoked gouda"]
vegetable_types = ["lettuce", "tomato", "onion", "cucumber", "spinach", "bell pepper", "olives", "jalapenos",
                   "mushrooms", "avocado", "sprouts", "cabbage", "carrots", "radishes", "pickles", "celery", "zucchini",
                   "beets", "chives", "broccoli"]
sauce_types = ["mayonnaise", "mustard", "ketchup", "ranch dressing", "honey mustard", "bbq sauce", "hot sauce", "pesto",
               "hummus", "sour cream", "tzatziki sauce", "sriracha", "thousand island dressing", "hoisin sauce",
               "teriyaki sauce", "guacamole", "wasabi", "tahini", "soy sauce", "chimichurri sauce"]


# Define the function for generating a sandwich
def generate_sandwich():
    bread = random.choice(bread_types)
    meat = random.choice(meat_types)
    cheese = random.choice(cheese_types)
    vegetable = random.choice(vegetable_types)
    sauce = random.choice(sauce_types)
    sandwich = [bread, meat, cheese, vegetable, sauce]
    return sandwich


# Define the function for handling the /sandwich command
def sandwich(update, context):
    chat_id = update.message.chat_id
    sandwich = generate_sandwich()
    sandwich_text = "\n".join(sandwich)
    context.bot.send_message(chat_id=chat_id, text=sandwich_text)


# Define the function for handling unknown commands
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# Set up the bot
bot_token = '5998014937:AAHC0Y_ZiPFjHDjltx8y3P8TV6sEyAwDXtg'
update_queue = queue.Queue()
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# def main() -> None:
# updater = Updater('5998014937:AAHC0Y_ZiPFjHDjltx8y3P8TV6sEyAwDXtg', update_queue=update_queue)


# Add the command handlers
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CallbackQueryHandler(language_callback))

sandwich_handler = CommandHandler('sandwich', sandwich)
dispatcher.add_handler(sandwich_handler)

# Add the unknown command handler
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

# Start the bot
updater.start_polling()
# Keep the bot running until the user stops the script with Ctrl-C
updater.idle()

if __name__ == "__main__":
    main()