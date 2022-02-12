import telebot
import config
import dbworker
from model import return_image
from torchvision.utils import save_image
import os
import shutil
from flask import Flask, request

TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
IS_PROCESSING = False

id_images_dict = {}
id_style_dict = {}

folder = 'images/'


@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_SEND_PIC.value:
        bot.send_message(message.chat.id, config.Messages.M_SEND_PIC.value)
    elif state == config.States.S_SEND_STYLE.value:
        bot.send_message(message.chat.id, config.Messages.M_SEND_STYLE.value)
    elif state == config.States.S_PROCESSING.value:
        bot.send_message(message.chat.id, config.Messages.M_PROCESSING.value)
    else:
        bot.send_message(message.chat.id, config.Messages.M_START.value)
        dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)


@bot.message_handler(commands=["help"])
def cmd_start(message):
    bot.send_message(message.chat.id, config.Messages.M_HELP.value)


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, config.Messages.M_START.value)
    dbworker.set_state(message.chat.id, config.States.S_SEND_PIC.value)


@bot.message_handler(content_types=["photo"],
                     func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_PIC.value)
def get_pic(message):
    try:
        raw = message.photo[1].file_id
        got_image_name = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(folder + got_image_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        id_images_dict[message.chat.id] = folder + got_image_name
        bot.send_message(message.chat.id, config.Messages.M_PIC_RECIVED.value)
        dbworker.set_state(message.chat.id, config.States.S_SEND_STYLE.value)
    except:
        error = config.Messages.E_SEND_PIC.value
        print(error)
        bot.send_message(message.chat.id, error)


@bot.message_handler(content_types=["photo"],
                     func=lambda message: dbworker.get_current_state(
                         message.chat.id) == config.States.S_SEND_STYLE.value)
def get_style(message):
    try:
        raw = message.photo[1].file_id
        got_style_name = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(folder + got_style_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        id_style_dict[message.chat.id] = folder + got_style_name

        bot.send_message(message.chat.id, config.Messages.M_STYLE_RECIVED.value)
        bot.send_message(message.chat.id, config.Messages.M_PROCESSING.value)
        dbworker.set_state(message.chat.id, config.States.S_PROCESSING.value)
    except:
        error = config.Messages.E_SEND_STYLE.value
        print(error)
        bot.send_message(message.chat.id, error)
        return
    try:
        print("Procesing for ", message.chat.id)
        generated_image = return_image(
            id_images_dict[message.chat.id],
            id_style_dict[message.chat.id])
        save_image(generated_image, folder + str(message.chat.id) + ".png")

        bot.send_message(message.chat.id, config.Messages.M_RESULT.value)
        bot.send_photo(message.chat.id, open(folder + str(message.chat.id) + '.png', 'rb'))
        path = os.path.join(folder + str(message.chat.id) + '.png')
        os.remove(path)
        print("Done with ", message.chat.id)
        bot.send_message(message.chat.id, config.Messages.M_END.value)

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    except:
        error = config.Messages.E_PROCESSING.value
        print(error)
        bot.send_message(message.chat.id, error)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://style-bot-dls-2021-fall.herokuapp.com//' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))