import telebot
import random
from khayyam import JalaliDatetime
from gtts import gTTS
import qrcode

mybot = telebot.TeleBot("*********************************************")


@mybot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    mybot.reply_to(message, f"سلام {name}، خوش اومدی.برای آشنایی با ربات روی /help کلیک کن")



mymarkup = telebot.types.ReplyKeyboardMarkup(row_width=1 ,  resize_keyboard=True )
btn1 = telebot.types.KeyboardButton('New Game')

mymarkup.add(btn1)


@mybot.message_handler(commands=['game'])
def game(message):
    mybot.reply_to(message, 'یک عدد حدس بزن بین 0 و 50')
    mybot.register_next_step_handler(message, game_play)


bot_num = random.randint(0, 50)


def game_play(message):
    if int(message.text) == bot_num:
        mybot.send_message(message.chat.id, 'درست حدس زدی! برنده شدی:)')
        mybot.number = random.randint(0, 20)
        mes = mybot.send_message(message.chat.id, 'برای یازی مجدد New Game رو بزن', reply_markup=mymarkup)
        mybot.register_next_step_handler(mes, game)

    elif int(message.text) > bot_num:
        mybot.send_message(message.chat.id, 'بیا پایین ')
        mybot.register_next_step_handler(message, game_play)

    elif int(message.text) < bot_num:
        mybot.send_message(message.chat.id, 'برو بالا')
        mybot.register_next_step_handler(message, game_play)


@mybot.message_handler(commands=['age'])
def Birthday(message):
    a = {}
    mybot.reply_to(message, 'تاریخ تولد را وارد کن:\n مثلا: 1401/1/1')
    mybot.register_next_step_handler(message, age)


def age(message):
    b = message.text.split('/')
    print(b)
    print(JalaliDatetime.now())
    age = JalaliDatetime.now() - JalaliDatetime(int(b[0]), int(b[1]), int(b[2]))

    mybot.send_message(message.chat.id, f'این شخص {age}  است')


@mybot.message_handler(['voice'])
def voice(message):
    mybot.reply_to(message, 'یک جمله انگیلیسی برام بفرست')
    mybot.register_next_step_handler(message, converttxtvc)


def converttxtvc(message):
    language = 'en'
    myobj = gTTS(text=message.text, lang=language, slow=False)
    myobj.save("voice.mp3")
    voice = open('voice.mp3', 'rb')
    mybot.send_voice(message.chat.id, voice)

@mybot.message_handler(['max'])
def input_nums(message):
    mybot.reply_to(message, 'لیست اعداد رو وارد کن\nمثلا: 1,2,3,4')
    mybot.register_next_step_handler(message, max_finder)


def max_finder(message):
    mynumberes = message.text.split(',')
    list = []
    for i in mynumberes:
        list.append(int(i))
    mybot.send_message(message.chat.id, f'بیشترین مقدار {max(list)} است')

@mybot.message_handler(['argmax'])
def input_nums(message):
    mybot.reply_to(message, 'لیست اعداد رو وارد کن\nمثلا: 1,2,3,4')
    mybot.register_next_step_handler(message, argmax_finder)


def argmax_finder(message):
    mynumberes = message.text.split(',')
    list = []
    for i in mynumberes:
        list.append(int(i))
    mybot.send_message(message.chat.id, f' اندیس بیشترین مقدار {list.index(max(list))} است')
    


@mybot.message_handler(['qrcode'])
def inputsen(message):
    mybot.reply_to(message, 'یک جمله برام بنویس')
    mybot.register_next_step_handler(message, makeqrcode)

def makeqrcode(message):
    img = qrcode.make(message.text)
    img.save('qrcode.png')
    image = open('qrcode.png', 'rb')
    mybot.send_photo(message.chat.id, image)

@mybot.message_handler(commands= ['help'])
def show_max(message):
    mybot.reply_to(message, 'لطفا انتخاب کنید:\n/game بازی اعداد\n/age محاسبه سن.\n/voice تبدیل جمله به صوت\n/max پیدا کردن بیشترین مقدار در لیست اعداد\n/argmax پیدا کردن اندیس بیشترین مقدار در لیست اعداد\n/qrcode تبدیل جمله به QR code')







mybot.polling()
