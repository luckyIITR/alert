from bot import telegram_chatbot
import wikipedia
bot = telegram_chatbot("config.cfg")
import random

def make_reply(msg):
    reply = None
    if msg is not None:
        result_set = wikipedia.search(msg, 5, suggestion=False)
        for term in result_set:
            try:
                reply = wikipedia.summary(term,sentences=1)
                return reply
            except wikipedia.DisambiguationError as e:
                pass
            except wikipedia.exceptions.PageError as error:
                pass
    return ("IDK")
flag = 0
update_id = None
while True:
    try : 
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                # print(update_id)
                try:
                    message = str(item["message"]["text"])
                    print(message)
                    # if message == "Exit":
                    #     flag = 1
                    #     break
                        
                except:
                    message = None
                from_ = item["message"]["from"]["id"]
                reply = make_reply(message)
                bot.send_message(reply, from_)
    except KeyboardInterrupt:
        exit()