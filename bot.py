from credentials import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types
from quiz import Quiz


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
quizzes_database = {}

# Handler to a command /start
@dp.message_handler(commands=['start']) 
async def send_welcome(message: types.Message):

    kb = [
        [
        types.KeyboardButton(text='/fast_quiz'), 
        types.KeyboardButton(text='/help'),
        types.KeyboardButton(text='/fast_poll')
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply('Hello!\nI am a polling bot!\nI can make polls in telegram.', reply_markup=keyboard) #Так как код работает 
асинхронно, то обязательно пишем await.
 
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
async def fast_qz(message: types.Message):
   qz_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   qz_keyboard.add(types.KeyboardButton(text="Create a quiz",
                                           request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
   qz_keyboard.add(types.KeyboardButton(text="Cancel"))
   await message.answer("Click the button below and create a quiz!!", reply_markup=qz_keyboard)

# Handler to a command /fast_poll
@dp.message_handler(commands=["fast_poll"])
async def fast_poll(message: types.Message):
   poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   poll_keyboard.add(types.KeyboardButton(text="Create a poll",
                                           request_poll=types.KeyboardButtonPollType(type='regular')))
   poll_keyboard.add(types.KeyboardButton(text="Cancel"))
   await message.answer("Click the button below and create a poll!", reply_markup=poll_keyboard)

# Handler to a text message "Cancel"
@dp.message_handler(lambda message: message.text == "Cancel")
async def action_cancel(message: types.Message):
   remove_keyboard = types.ReplyKeyboardRemove()
   await message.answer("The action is canceled. Enter the command to start over.", reply_markup=remove_keyboard)

# @dp.message_handler(commands=["poll"]) 
# async def poll(message: types.Message):
#    qw = '',
#    opt = []
#    await message.answer("Send me your question:")
#    qw = message.text

#     quizzes_database[str(message.from_user.id)].append(Quiz(
#         question=qw
#         options=opt,
#         correct_option_id=message.poll.correct_option_id,
#         owner_id=message.from_user.id)
#     )


#    await bot.send_poll(chat_id=message.from_user.id, 
#                        question='Your answer?',                     
#                        options=['A)', 'B)', 'C'],                     
#                        type='quiz',                     
#                        correct_option_id=1)

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
