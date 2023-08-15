from credentials import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types

from messages import help_message, start_message, quiz_message, poll_message


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

quizzes_database = {}

# States declaration
class State:
   QUESTION = 0
   ANSWERS = 1
   POLL_TYPE = 2
   POLL = 3
   POLL_ERROR = 4
   QUESTION_QUIZ = 5
   ANSWERS_QUIZ = 6
   QUIZ_TYPE = 7
   CORRECT_ANS = 8
   QUIZ = 9


user_state = {}

qw_dict = {}
ans_dict = {}
type_dict = {}
cor_ans_dict = {}

def set_state(user_id: int, state: int):
   user_state[user_id] = state

def get_user_state(user_id: int):
   if not user_id in user_state:
      user_state[user_id] = State.QUESTION
   return user_state[user_id]

# Handler to a command /start
@dp.message_handler(commands=['start']) 
async def send_welcome(message: types.Message):
   start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   start_keyboard.add(types.KeyboardButton(text='/fast_quiz'))
   start_keyboard.add(types.KeyboardButton(text='/fast_poll'))
   start_keyboard.add(types.KeyboardButton(text='/help'))
   start_keyboard.add(types.KeyboardButton(text='/poll'))
   start_keyboard.add(types.KeyboardButton(text='/quiz'))

   await message.reply(start_message, reply_markup=start_keyboard) 

# Handler to a command /help
@dp.message_handler(commands=["help"])
async def help_func(message: types.Message):
   help_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
   help_keyboard.add(types.KeyboardButton(text="/fast_quiz"))
   help_keyboard.add(types.KeyboardButton(text="/fast_poll"))
   help_keyboard.add(types.KeyboardButton(text="Cancel"))
   await message.answer( reply_markup=help_keyboard)


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


# Handler to a command /poll
@dp.message_handler(commands=["poll"]) 
async def poll(message: types.Message):
   user_id = message.from_user.id
   await message.answer("Send me your question:")
   set_state(user_id, State.QUESTION)


async def question_parse(message: types.Message):
   user_id = message.from_user.id
   qw_dict[user_id] = message.text
   await message.answer("Send me your answers. Use ';' as a separator please.")
   set_state(user_id, State.ANSWERS)


async def answers_parse(message: types.Message):
   user_id = message.from_user.id
   if ';' in message.text:
      ans_dict[user_id] = message.text
      await message.answer('Do you want to have an anonymous poll?\nSend "YES" or "NO".')
      set_state(user_id, State.POLL_TYPE)
   else:
      poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
      poll_keyboard.add(types.KeyboardButton(text="/poll"))
      poll_keyboard.add(types.KeyboardButton(text="Cancel"))
      await message.reply('Sorry, wrong format. Start again, please.', reply_markup=poll_keyboard)


async def type_parse(message: types.Message):
   user_id = message.from_user.id
   type_text = message.text
   if type_text == 'YES' or type_text == 'Yes' or type_text == 'yes':
      type_dict[user_id] = True
   else:
      type_dict[user_id] = False
   await message.answer(poll_message.format(qw_dict[user_id], ans_dict[user_id], type_dict[user_id]))
   set_state(user_id, State.POLL)


async def sending_poll(message: types.Message):
   type_text = message.text
   user_id = message.from_user.id
   if type_text == 'YES' or type_text == 'Yes' or type_text == 'yes':
      await bot.send_poll(chat_id=user_id, 
                       question=qw_dict[user_id],                     
                       options=ans_dict[user_id].split(sep=';'),                     
                       type='regular',                     
                       is_anonymous=type_dict[user_id])
   elif type_text == 'NO' or type_text == 'No' or type_text == 'no':
      user_id = message.from_user.id
      await message.answer(f"Let's start from the beggining. Send me your question.")
      set_state(user_id, State.QUESTION) 


# Handler to a command /quiz
@dp.message_handler(commands=["quiz"]) 
async def poll(message: types.Message):
   user_id = message.from_user.id
   await message.answer("Send me your question:")
   set_state(user_id, State.QUESTION_QUIZ)

async def question_parse_quiz(message: types.Message):
   user_id = message.from_user.id
   qw_dict[user_id] = message.text
   await message.answer("Send me your answers. Use ';' as a separator please.")
   set_state(user_id, State.ANSWERS_QUIZ)


async def answers_parse_quiz(message: types.Message):
   user_id = message.from_user.id
   if ';' in message.text:
      ans_dict[user_id] = message.text
      await message.answer('Do you want to have an anonymous quiz?\nSend "YES" or "NO".')
      set_state(user_id, State.QUIZ_TYPE)
   else:
      quiz_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
      quiz_keyboard.add(types.KeyboardButton(text="/quiz"))
      quiz_keyboard.add(types.KeyboardButton(text="Cancel"))
      await message.reply('Sorry, wrong format. Start again, please.', reply_markup=quiz_keyboard)



async def type_parse_quiz(message: types.Message):
   user_id = message.from_user.id
   type_text = message.text
   if type_text == 'YES' or type_text == 'Yes' or type_text == 'yes':
      type_dict[user_id] = True
   else:
      type_dict[user_id] = False
   await message.answer('Send me an index of a correct answer (starting from 0), please.')   
   set_state(user_id, State.CORRECT_ANS)

async def correct_ans_parse(message: types.Message):
   user_id = message.from_user.id
   type_text = message.text
   cor_ans_dict[user_id] = type_text
   await message.answer(quiz_message.format(qw_dict[user_id], ans_dict[user_id], type_dict[user_id], cor_ans_dict[user_id]))
   set_state(user_id, State.QUIZ)


async def sending_quiz(message: types.Message):
   type_text = message.text
   user_id = message.from_user.id
   if type_text == 'YES' or type_text == 'Yes' or type_text == 'yes':
      await bot.send_poll(chat_id=user_id, 
                       question=qw_dict[user_id],                     
                       options=ans_dict[user_id].split(sep=';'),                     
                       type='quiz',
                       correct_option_id = cor_ans_dict[user_id],                     
                       is_anonymous = type_dict[user_id])
   elif type_text == 'NO' or type_text == 'No' or type_text == 'no':
      user_id = message.from_user.id
      await message.answer(f"Let's start from the beggining. Send me your question.")
      set_state(user_id, State.QUESTION_QUIZ) 
    


@dp.message_handler()
async def text_handler(message: types.Message):
   user_id = message.from_user.id
   if get_user_state(user_id) == State.QUESTION:
      await question_parse(message)
   elif get_user_state(user_id) == State.ANSWERS:
      await answers_parse(message)
   elif get_user_state(user_id) == State.POLL_TYPE:
      await type_parse(message)
   elif get_user_state(user_id) == State.POLL: 
      await sending_poll(message)
   elif get_user_state(user_id) == State.QUESTION_QUIZ:
      await question_parse_quiz(message)
   elif get_user_state(user_id) == State.ANSWERS_QUIZ:
      await answers_parse_quiz(message)
   elif get_user_state(user_id) == State.QUIZ_TYPE:
      await type_parse_quiz(message)
   elif get_user_state(user_id) == State.CORRECT_ANS: 
      await correct_ans_parse(message)
   elif get_user_state(user_id) == State.QUIZ: 
      await sending_quiz(message)
   else:
      await message.answer("Something got wrong :(")


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
