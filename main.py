from src.card import del_file, create_card
from src.utils import del_buttons
from static.buttons import check_group, new_form, edit_data
from src.user import User
from static.phrases import phrases, sequence
from src.send_mail import send_mail, send_to_chat
from config.config import config

from dialog_bot_sdk.bot import DialogBot
import grpc
import os


users = {}


def on_msg(*params):
    peer = params[0].peer
    id_ = peer.id

    if id_ not in users:
        users[peer.id] = User(peer.id)

    user = users[peer.id]

    if user.lock_msg:
        return

    last_key = user.last_key
    text = params[0].message.textMessage.text

    if peer.type == 1:
        if last_key == "":
            user.last_key = "hello"
            bot.messaging.send_message(peer, phrases["hello"])
        elif "check" in last_key:
            if "to_check" in last_key:
                user.filling_data(last_key[9:], text)
            msg = phrases["check"] + "\n" + user.form()
            group = check_group()
            bot.messaging.send_message(peer, msg, group)
            user.lock_msg = True
        else:
            user.filling_data(last_key, text)
            next_key = sequence[last_key]
            user.last_key = next_key
            next_msg = phrases[next_key]
            if next_key == "check":
                next_msg = phrases[next_key] + "\n" + user.form()
                group = check_group()
                bot.messaging.send_message(peer, next_msg, group)
            elif next_key == "surname":
                bot.messaging.send_message(peer, next_msg.format(text))
            else:
                bot.messaging.send_message(peer, next_msg)


def on_click(*params):
    uid = params[0].uid
    peer = bot.users.get_user_peer_by_id(uid)
    if uid not in users:
        users[uid] = User(uid)
        users[uid].last_key = "hello"
        bot.messaging.send_message(peer, phrases["hello"])
        return
    user = users[uid]

    which_button = params[0].value
    if which_button == "Yes":
        del_buttons(bot, peer)
        files = create_card(user)
        print(send_mail(user.e_mail, files))
        print(send_to_chat(bot, peer, files[0]))
        del_file(files)
        bot.messaging.send_message(
            peer,
            "Письмо с визиткой отправлено на вашу почту {0}!\nЕсли хотите создать новую визитку, нажмите на кнопку."
                                   .format(user.e_mail),
            new_form()
        )
        user.lock_msg = True
        return
    elif which_button == "No":
        group = edit_data()
        del_buttons(bot, peer)
        bot.messaging.send_message(peer, "Что Вы хотели бы исправить?", group)
        user.lock_msg = True
        return
    elif which_button == "all":
        user.last_key = "second_name"
        del_buttons(bot, peer)
        bot.messaging.send_message(peer, phrases["second_name"])
    else:
        user.last_key = "to_check_" + which_button
        del_buttons(bot, peer)
        bot.messaging.send_message(peer, phrases[which_button])
    user.lock_msg = False


if __name__ == '__main__':
    cfg = config["bot_config"]
    bot = DialogBot.get_secure_bot(
        os.environ[cfg["endpoint"]],
        grpc.ssl_channel_credentials(),
        os.environ[cfg["token"]]
    )
    bot.messaging.on_message_async(on_msg, on_click)
