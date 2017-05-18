import json
import urllib.request

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.73ffab01-a6bc-4fc1-bdbb-c1a7c2e68fd0"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def get_welcome_response():
    session_attributes = {}
    card_title = "Mubashir Good News"
    speech_output = "Welcome to the Alexa Mubashir Good News skill. " \
                    "You can ask me for recent uplifting news, or " \
                    "ask me for other features that I haven't implemented yet! "\
    reprompt_text = "Please ask me for good news, " \
                    "for example tell me good news."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def on_session_started(session_started_request, session):
    print("Starting new session.")

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetGoodNews":
        return get_good_news(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(intent)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def get_good_news(intent):
    session_attributes = {}
    card_title = "Mubashir Get Good News"
    speech_output = "Welcome to good news. The hottest uplifting news on reddit will be relayed to you."
    reprompt_text = ""
    should_end_session = False

    num_stories = 3
    TARGET = "https://reddit.com/r/UpliftingNews/hot.json?limit=%d" % num_stories
    # also top.json, new.json available

    # get the data and load into JSON
    req = urllib.request.Request(TARGET, method='GET')
    req.add_header('User-Agent', 'web app:T9CS8svlPtNOlw:0.1 (by /u/samhavron)')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    tmp = ''
    if not resp:
      print("Error retrieving uplifting news from '%s' on Reddit\n" % TARGET)
    else:
      for i in range(num_stories):
	tmp += "Hot story #%d:\n" % (i+1) + resp["data"]["children"][i]["data"]["title"]) 

    speech_output = tmp

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

## do not need to edit anything below this line!
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }

def handle_session_end_request():
    card_title = "Mubashir - Thanks"
    speech_output = "Thank you for using the Mubashir skill. See you next time!"
    should_end_session = True
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))
