import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App
import requests
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Event API & Web API
app = App(token=os.environ['SLACK_BOT_TOKEN']) 
client = WebClient(os.environ['SLACK_BOT_TOKEN'])

# This gets activated when the bot is tagged in a channel    
@app.event("app_mention")
def handle_message_events(body, logger):
    # Create prompt for API
    prompt = str(body["event"]["text"]).split(">")[1]
    print('Q:', prompt)
    
    # Let thre user know that we are busy with the request 
    # response = client.chat_postMessage(channel=body["event"]["channel"], 
    #                                    thread_ts=body["event"]["event_ts"],
    #                                    text=f"Calculating... :robot_face: \n")
    
    # Check API
    datainput = json.dumps({"params":{"question":prompt},"project":os.environ['RELEVANCEAI_PROJECT']})
    response = requests.post(os.environ['RELEVANCEAI_API_ENDPOINT'], data = datainput, headers={"content-type": "application/json"})

    print('A', response.json()['output']['answer'])

    # Reply to thread 
    response = client.chat_postMessage(channel=body["event"]["channel"], 
                                       thread_ts=body["event"]["event_ts"],
                                       text=f":robot_face: {response.json()['output']['answer']}")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ['SLACK_APP_TOKEN']).start()

