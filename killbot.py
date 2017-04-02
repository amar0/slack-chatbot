import os
import time
from slackclient import SlackClient

import webbrowser
import subprocess
url = 'http://www.google.com/'
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

BOT_ID = os.environ.get('BOT_ID')

AT_BOT = "<@" + BOT_ID + ">:"

COMMAND = [("hello", "hi"), "how", "can","who",("fuck","asshole","stupid","idiot"),("open","google","search"),"maps","music","telegram"]

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
	response = "Not sure what you meant."
	if command.startswith(COMMAND[0]):
		response = "Hello! How can I help you?"
	elif command.startswith(COMMAND[1]):
		response = "I'm fine how are you?"
	elif command.startswith(COMMAND[2]):
		response = "Yeah!! Sure"
	elif command.startswith(COMMAND[3]):
		response = "Hi I'm Killbot :)"
	elif command.startswith(COMMAND[4]):
		response = "mind your language please"
	elif command.startswith(COMMAND[5]):
		response = webbrowser.get(chrome_path).open(url)
	elif command.startswith(COMMAND[6]):
		response = subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/Maps.app"])
	elif command.startswith(COMMAND[7]):
		response = subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/iTunes.app"])
	elif command.startswith(COMMAND[8]):
		response = subprocess.call(["/usr/bin/open", "-W", "-n", "-a", "/Applications/Telegram.app"])
	slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
	output_list = slack_rtm_output
	if output_list and len(output_list) > 0:
		for output in output_list:
			if output and 'text' in output and AT_BOT in output['text']:
				return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
	return None, None

if __name__ == "__main__":
	READ_WEBSOCKET_DELAY = 1
	if slack_client.rtm_connect():
		print("KillBot connected and running!")
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token or bot ID?")