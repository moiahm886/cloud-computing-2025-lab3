import json
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# Use /mnt/data.json instead of data.json directly
DATA_FILE_PATH = '/mnt/data.json'

def read_messages_from_file():
    with open(DATA_FILE_PATH) as messages_file:
        return json.load(messages_file)

def append_message_to_file(content):
    data = read_messages_from_file()
    new_message = {
        'content': content,
        'timestamp': datetime.now().isoformat(" ", "seconds")
    }
    data['messages'].append(new_message)
    with open(DATA_FILE_PATH, mode='w') as messages_file:
        json.dump(data, messages_file)

@app.route("/")
def home():
    new_message = request.args.get('msg')
    if new_message:
        append_message_to_file(new_message)

    data = read_messages_from_file()
    return render_template('home.html', messages=data['messages'])

# This part is critical for Docker
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
