import copy
import os
import re
import unittest
from dialog_bot_sdk.bot import DialogBot

import grpc
from mock import patch

from config.config import config
from src.card import create_card, del_file
from src.send_mail import get_message, send_mail, send_to_chat
from src.user import User

user1 = User(1, "Event", "Bot", "dialog", "bot", "event_bot@dlg.im", "+7-888-888-88-88")
user2 = User(2)
file1 = "test_card.svg"
regexp = r'>([\w0-9\.\-\_\@]+)</tspan>|<text .+>(\w+)</text>'
old_cfg = copy.deepcopy(config)


class MyTestCase(unittest.TestCase):
    def test_full_user(self):
        self.assertEqual(user1.is_full_profile(), True)
        user2 = User(2)
        self.assertEqual(user2.is_full_profile(), False)

    def test_form(self):
        self.assertEqual("Event Bot\ndialog\nbot\nevent_bot@dlg.im\n+7-888-888-88-88", user1.form())

    def test_filling_data(self):
        user2.filling_data("hello", "Ev")
        user2.filling_data("surname", "bot")
        user2.filling_data("org", "dialog")
        user2.filling_data("post", "bot")
        user2.filling_data("e-mail", "event_bot@dlg.im")
        user2.filling_data("phone", "+7-888-888-88-88")
        self.assertNotEqual(user1.form(), user2.form())
        user2.filling_data("second_name", "Event")
        user2.filling_data("second_surname", "Bot")
        self.assertEqual(user1.form(), user2.form())

    def test_create_card_and_del_file(self):
        config["template"] = "../static/template.svg"
        files = create_card(user1)
        self.assertEqual(os.path.exists(files[0]), True)
        self.assertEqual(os.path.exists(files[1]), True)
        file = files[1]
        test = []
        arr = []
        l = 0
        with open(file1) as f:
            for line in f:
                if 13 <= l <= 16:
                    test.append(re.findall(regexp, line))
                l += 1
        l = 0
        with open(file) as f:
            for line in f:
                if 13 <= l <= 16:
                    arr.append(re.findall(regexp, line))
                l += 1
        self.assertEqual(test, arr)
        del_file(files)
        self.assertEqual(os.path.exists(files[0]), False)
        self.assertEqual(os.path.exists(files[1]), False)

    def test_get_msg(self):
        msg = get_message("mail", file1, config["email_config"])
        self.assertEqual(msg._headers, [('Content-Type', 'multipart/mixed'), ('MIME-Version', '1.0'),
                                        ('Subject', 'dialog: ваша визитная карточка'),
                                        ('From', 'MAIL_LOGIN'), ('To', 'mail')])

    def test_send_mail_off(self):
        config["email_config"]["to_mail"] = False
        res = send_mail(user1.e_mail, file1)
        self.assertEqual("E-mail not sent due to settings of config", res)

    def test_send_to_chat_off(self):
        config["email_config"]["to_chat"] = False
        res = send_to_chat("bot", "peer", file1)
        self.assertEqual("File not sent due to settings of config", res)

    def test_send_mail(self):
        config["email_config"]["to_mail"] = True
        with patch('src.send_mail.login_and_send') as perm_mock:
            perm_mock.return_value = 1
            self.assertEqual(send_mail(user1.e_mail, [file1]), "E-mail sent successfully")

    def test_send_to_chat(self):
        config["email_config"]["to_chat"] = True
        cfg = config["bot_config"]
        bot = DialogBot.get_secure_bot(
            os.environ[cfg["endpoint"]],
            grpc.ssl_channel_credentials(),
            os.environ[cfg["token"]]
        )
        with patch('dialog_bot_sdk.messaging.Messaging.send_file') as perm_mock:
            perm_mock.return_value = 1
            self.assertEqual(send_to_chat(bot, "peer", file1), "File sent to chat")


if __name__ == '__main__':
    unittest.main()
    config = old_cfg
