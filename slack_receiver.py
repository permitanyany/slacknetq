import os
import subprocess
import re
from flask import Flask, request, Response
from slackclient import SlackClient


app = Flask(__name__)
slack_client = SlackClient('xyz')

def send_message(channel_id, message):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        username='NetQ Bot',
        icon_emoji=':turtle:'
    )

@app.route('/', methods=['GET'])
def test():
    return Response('Test Successful')

@app.route('/slack', methods=['POST'])
def inbound():
        channel_name = request.form.get('channel_name')
        channel_id = request.form.get('channel_id')
        username = request.form.get('user_name')
        inbound_command = request.form.get('text')
        p = subprocess.Popen(("netq " + inbound_command), stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
	color_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        send_message(channel_id, ("`" + "netq " + inbound_command + "`"))
        send_message(channel_id, ("```" + color_escape.sub('', output) + "```"))
        return Response(), 200

if __name__ == "__main__":
    app.run(port=1234, debug=True)

