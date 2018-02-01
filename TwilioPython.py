from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import constants
app = Flask(__name__)

account_sid = constants.ACCOUNT_SID
auth_token = constants.AUTH_TOKEN
client = Client(account_sid, auth_token)

visits = 0


@app.route("/")
def new_visit():
    global visits
    visits += 1

    client.messages.create(
        to=constants.MY_PHONE_NUMBER,
        from_=constants.TWILIO_PHONE_NUMBER,
        body="Hello Visitor #" + str(visits) + "! To make us forget your last visit, "
                                               "reply with \"Forget it!\" "
                                               "(quotes not included)."
    )
    # not sure what the best way to return an ok response is, this will do for now
    return "OK"


# should request mappings be separated by file for sake of "best practices"? If so, how?
@app.route("/sms", methods=["POST"])
def sms():
    body = request.values.get('Body', None)
    resp = MessagingResponse()

    if body == "Forget it!" and visits > 0:
        forget_visit()
        resp.message("Your visit has been forgotten!")
    else:
        resp.message("Invalid message!")

    return str(resp)


def forget_visit():
    global visits

    if visits > 0:
        visits -= 1

if __name__ == '__main__':
    app.run()
