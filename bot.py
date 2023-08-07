from credentials import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

quizzes_database = {}

# States declaration
class State:
   QUESTION = 0
   ANSWERS = 1
   POLL_TYPE = 2
   POLL = 3


user_state = {}

qw_dict = {}
ans_dict = {}
type_dict = {}

def set_state(user_id: int, state: int):
   user_state[user_id] = state

def get_user_state(user_id: int):
   if not user_id in user_state:
      user_state[user_id] = State.QUESTION
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
   ans_dict[user_id] = message.text
   await message.answer('Do you want to have an anonymous poll?\nSend "YES" or "NO".')
   set_state(user_id, State.POLL_TYPE)


async def type_parse(message: types.Message):
   user_id = message.from_user.id
   type_text = message.text
   if type_text == 'YES':
      type_dict[user_id] = True
   else:
      type_dict[user_id] = False
   await message.answer(f'Let me see if I have understood you right:\nYour question: {qw_dict[user_id]}\nAnswers: {ans_dict[user_id]}.\nIs anonymous: {type_dict[user_id]}.\nAnswer me "YES" if everything is correct or "NO" if you want to correct something.')
   set_state(user_id, State.POLL)


async def sending_poll(message: types.Message):
   type_text = message.text
   user_id = message.from_user.id
   if type_text == 'YES':
      await bot.send_poll(chat_id=user_id, 
                       question=qw_dict[user_id],                     
                       options=ans_dict[user_id].split(sep=';'),                     
                       type='regular',                     
                       is_anonymous=type_dict[user_id])



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
   else:
      await message.answer("Something got wrong :(")


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)
