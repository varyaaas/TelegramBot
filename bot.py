import logging

from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = 'YOUR TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Handler to a command /start
@dp.message_handler(commands=['start']) 
async def send_welcome(message: types.Message):

    kb = [
        [
        types.KeyboardButton(text='/fast_quiz'), 
        types.KeyboardButton(text='/help')
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply('Hello!\nI am a polling bot!\nI can make polls in telegram.', reply_markup=keyboard) 
 
# Handler to a command /help
@dp.message_handler(commands=["help"])
async def help_func(message: types.Message):
   help_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   help_keyboard.add(types.KeyboardButton(text="/fast_quiz"))
   help_keyboard.add(types.KeyboardButton(text="/fast_poll"))
   help_keyboard.add(types.KeyboardButton(text="Cancel"))
   await message.answer("""I am able to make quizes and polls.\n\nTo make a fast quiz use /fast_quiz command.
                         \nTo make a fast poll use /fast_poll command.""", reply_markup=help_keyboard)

# Handler to a command /fast_quiz
@dp.message_handler(commands=["fast_quiz"])
async def cmd_start(message: types.Message):
   poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   poll_keyboard.add(types.KeyboardButton(text="Create a quiz",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
   poll_keyboard.add(types.KeyboardButton(text="Cancel"))
   await message.answer("Click the button below and create a quiz!!", reply_markup=poll_keyboard)


# Handler to a text message "Cancel"
@dp.message_handler(lambda message: message.text == "Cancel")
async def action_cancel(message: types.Message):
   remove_keyboard = types.ReplyKeyboardRemove()
   await message.answer("The action is canceled. Enter the command to start over.", reply_markup=remove_keyboard)



if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
