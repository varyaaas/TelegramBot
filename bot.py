from credentials import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types
# from quiz import Quiz


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

quizzes_database = {}

# States declaration
class State:
   QUIZ = 0
   QUESTION = 1
   ANSWERS = 2
   TYPE = 3
   POLL = 4


user_state = {}

def set_state(user_id: int, state: int):
   user_state[user_id] = state

def get_user_state(user_id: int):
   if not user_id in user_state:
      user_state[user_id] = State.QUIZ
   return user_state[user_id]

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


@dp.message_handler(commands=["poll"]) 
async def poll(message: types.Message):
   user_id = message.from_user.id
   set_state(user_id, State.QUESTION)
   await message.answer("Send me your question:")



@dp.message_handler()
async def question_parse(message: types.Message):
   user_id = message.from_user.id
   qw_text = message.text
   set_state(user_id, State.ANSWERS)
   await message.answer("Send me your answers. Use ';' as a separator.")


@dp.message_handler()
async def answers_parse(message: types.Message):
   await message.answer("Do you want to have an anonymous poll? Send 'YES' or 'NO'.")
   user_id = message.from_user.id
   ans_text = message.text
   ans = ans_text.split(';')
   set_state(user_id, State.TYPE)
   await message.answer("Do you want to have an anonymous poll? Send 'YES' or 'NO'.")
  
@dp.message_handler()
async def type_parse(message: types.Message):
   user_id = message.from_user.id
   type_text = message.text
   if type_text == 'YES':
      tp = True
   else:
      tp = False
   set_state(user_id, State.POLL)


@dp.message_handler()
async def sending_poll(message: types.Message):
   await bot.send_poll(chat_id=message.from_user.id, 
                       question=qw_text,                     
                       options=ans,                     
                       type='poll',                     
                       is_anonymous=tp)


@dp.message_handler()
async def text_handler(message: types.Message):
   user_id = message.from_user.id
   if get_user_state(user_id) == State.QUESTION:
      await question_parse(message)
   elif get_user_state(user_id) == State.ANSWERS:
      await answers_parse(message)
   elif get_user_state(user_id) == State.TYPE:
      await type_parse(message)
   elif get_user_state(user_id) == State.POLL: 
      await sending_poll(message)
   else:
      await message.answer("Something got wrong :(")



 #   qw = '',
 #   opt = []
 #   qw = message.text

 #    quizzes_database[str(message.from_user.id)].append(Quiz(
 #        question=qw
 #        options=opt,
 #        correct_option_id=message.poll.correct_option_id,
 #        owner_id=message.from_user.id)
 #    )



 # quizzes_database[str(message.from_user.id)].append(Quiz(
 #        question=qw_text,
 #        options=[],
 #        owner_id=user_id)
 #    )


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
