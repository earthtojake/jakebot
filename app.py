from flask import Flask, request
import msg
import time
from pymessenger.bot import Bot
import re

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAF4fQe12XQBALKJZAZAZC3Q1Kq56n1vuju5ZAngRciCFqlFVKT8EoHyFDKEy16UiZAaz78KUH31gEXDT6lfUbGT4oqP81GgYahUqRv0pmUtuwgmLlZBkSWf0cZA3e8B3WPmoQfJyHH3JG1MdPjeqnShKIZAbf8DeImhTPMCsxyX8QZDZD'
bot = Bot(PAT)

BROKEN_RESPONSE = "Oh no... I think you just broke me 😳 Sorry, there must be a bug in my code. I'll report this to real Jake right away! Message me again later! *bangs head*"

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == 'my_voice_is_my_password_verify_me':
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                print x
                recipient_id = x['sender']['id']
                bot.send_action(recipient_id,'typing_on')
                if x.get('message'):
                    if x['message'].get('text'):
                        send_response(recipient_id,x['message']['text'])
                    else:
                        bot.send_text_message(recipient_id,BROKEN_RESPONSE)
                elif x.get('postback'):
                    index = x['postback']['payload'] # 1.1.2, 3.4, etc
                    bot.send_text_message(recipient_id,'You pressed a button... payload = '+str(index))
                    # get response via index from apiai
                else:
                    bot.send_text_message(recipient_id,BROKEN_RESPONSE)
                    pass
                bot.send_action(recipient_id,'typing_off')
        return "Success"

def send_response(recipient_id,message):

  big_response = msg.respond(recipient_id,message)

  # send button options response
  if '[BTN]' in big_response:
    split = big_response.split('[BTN]')
    if len(split) == 2:
      pretext = split[0]
      response = split[1]

      button_txts = response.split('|')
      buttons = []
      for button_txt in button_txts:
        button = {
          "type":"postback",
          "title":button_txt.strip(),
          "payload":"payload goes here"
        }
        buttons.append(button)

      time.sleep(0.25)
      bot.send_button_message(recipient_id, pretext, buttons)
    else:
      bot.send_text_message(recipient_id,BROKEN_RESPONSE)

  # send text response
  else:
    for response in big_response.split('|'):
      time.sleep(0.25)
      bot.send_text_message(recipient_id, response)

if __name__ == '__main__':
  app.run()