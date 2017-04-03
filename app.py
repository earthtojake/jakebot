from flask import Flask, request
import requests
 
app = Flask(__name__)
 
ACCESS_TOKEN = "EAAF4fQe12XQBAOfF2ZBVTBy9TfrBJaKSl40H1Q0fYJfUZABOXiCYw2hmwEVMjGUXGSqzBQEOezNIe6t3GEv19izkD08dlgPIYcnavkIeZBFDfc15aShAMnCLBDgIpYC3e9ViYqLZAWexLaDqA9WPJxsSLXZBvFUwdplsUtlamoQZDZD"
 
@app.route('/', methods=['GET'])
def handle_verification():
    return request.args['hub.challenge']
 
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)
 
 
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message[::-1])
 
    return "ok"
 
 
if __name__ == '__main__':
    app.run(debug=True)