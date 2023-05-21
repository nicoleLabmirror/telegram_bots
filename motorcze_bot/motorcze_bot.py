#!/usr/bin/python3

import telepot as tb
import telepot.aio.loop
import telepot.loop

BOT = tb.Bot("BOT_TOKEN")
CHAT_ID = "CHAT_ID"


def read_message_from_user(msg):
    message_text = msg["text"]
    print("I read messages")
    handle_message(message_text)


def handle_message(message_text):
    text = message_text.split(" ")
    text = "test".join(text)
    print("I change messages")
    send_message(text)


def send_message(text):
    print("I send messages")
    BOT.sendMessage(CHAT_ID, text)


def main():
    print("I run the programm")
    telepot.loop.MessageLoop(BOT, read_message_from_user).run_forever()


if __name__ == "__main__":
    main()
