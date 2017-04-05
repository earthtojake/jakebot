from flask import Flask, request
import msg
from pymessenger.bot import Bot

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAF4fQe12XQBALKJZAZAZC3Q1Kq56n1vuju5ZAngRciCFqlFVKT8EoHyFDKEy16UiZAaz78KUH31gEXDT6lfUbGT4oqP81GgYahUqRv0pmUtuwgmLlZBkSWf0cZA3e8B3WPmoQfJyHH3JG1MdPjeqnShKIZAbf8DeImhTPMCsxyX8QZDZD'
bot = Bot(PAT)

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
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    bot.send_action(recipient_id,'typing_on')
                    if x['message'].get('text'):
                        message = x['message']['text']
                        bot.send_text_message(recipient_id, msg.respond(recipient_id,message))
                    bot.send_action(recipient_id,'typing_off')
                else:
                    pass
        return "Success"

if __name__ == '__main__':
  app.run()