from dialog_api import messaging_pb2


def del_buttons(bot, peer):
    outpeer = bot.manager.get_outpeer(peer)
    history = bot.messaging.load_message_history(outpeer, limit=10, direction=messaging_pb2.LISTLOADMODE_BACKWARD).history
    for msg in history:
        if msg.sender_uid != peer.id:
            return bot.messaging.update_message(msg, msg.message.textMessage.text)