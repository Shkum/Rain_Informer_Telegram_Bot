from time import sleep
import telebot
from Weather import Weather
import threading

# Create bot instance
bot = telebot.TeleBot('5433931992:AAG7ykhximKcgFz-SY6-zjNenTVQ7X4h0dQ')
weather = Weather()

command_flag = False

thread_exit_flag = False


# Function handling 'start' command
@bot.message_handler(commands=["start"])
def start(m):
    global command_flag
    bot.send_message(m.chat.id, 'Enter location name to start rain monitoring:')
    command_flag = True


@bot.message_handler(commands=["stop"])
def stop(m):
    global thread_exit_flag
    bot.send_message(m.chat.id, 'Rain monitoring stopped')
    thread_exit_flag = True


# Getting message from user
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global command_flag
    msg = message.text
    if command_flag:
        weather.set_location(msg)

        wtr = weather.check_weather()
        if wtr != 'City not found or connection error...':
            bot.send_message(message.chat.id, 'New location is: ' + msg)
            bot.send_message(message.chat.id, wtr[0])
            bot.send_message(message.chat.id, 'Rain: ' + str(wtr[1][1]))
            command_flag = False
            x = threading.Thread(target=loop_weather_check(message.chat.id), args=(1,))  # запускаем цикл в отдельном потоке на проверку погоды и передает функции id чата для ответе в канал
            x.start()
        else:
            bot.send_message(message.chat.id, 'City not found or connection error...')
            command_flag = False
    else:
        bot.send_message(message.chat.id, 'Your message is: ' + msg)


# loop function, which checking weather and report to telegram in case of rain
def loop_weather_check(chat_id):
    global thread_exit_flag
    while not thread_exit_flag:
        weather_loop = weather.check_weather()
        if weather_loop[1][1].keys():
            bot.send_message(chat_id, 'Rain: ' + str(*weather_loop[1][1].keys()))
            bot.send_message(chat_id, 'Monitoring stopped. Restart it if necessary.')
            thread_exit_flag = True
        sleep(3)
    thread_exit_flag = False
    bot.send_message(chat_id, 'Exit monitoring...')


# start bot
bot.polling(none_stop=True, interval=0)
