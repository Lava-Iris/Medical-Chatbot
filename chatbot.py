import pandas as pd
import re
import json
import unknown

def load_json(file):
    with open(file) as openedFile:
        print(f"Successfully loaded: '{file}'")
        return json.load(openedFile)

#symptoms = pd.DataFrame(columns = ["Symptom", "Probing question", "Diseases"]);
#diseases = pd.DataFrame(columns = ["Disease", "Symptoms", "Time Period", "Treatment"]);


symptoms = load_json("symptoms.json")
diseases = load_json("diseases.json")
greetResponses = load_json("greet.json")
map = pd.read_csv("medMap.csv")

def processInput(input, response_data):
    # Check if input is empty
    if input == "":
        returnOutput("Please type something so we can chat :(")
        return processInput(input = getInput(), response_data = response_data)

    split_input = re.split(r'\s+|[,;?!.-]\s*', input.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_input:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_input:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)


    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]

    returnOutput(unknown.unknown_string())
    return processInput(input = getInput(), response_data = response_data)

def bot():
    #greetings 0
    greeting = "Hello! Welcome to Apollo Hospitals. How are you feeling today?"
    def greet(input = ""):
        returnOutput(greeting)
        returnOutput(processInput(input = getInput(), response_data = greetResponses)["response"])
        diagnose(processInput(input=getInput(), response_data= symptoms))

    #diagnosis 1
    def diagnose(symptom):
        #make a list of diseases with that symptom
        #make a priority list of symptoms that we need to rule out with priority bring how close it is to 50%
        print(symptom);

    #treatment 2

    #ending 3



    response_functions = [greet, diagnose]

    greet()


def getInput(): 
    return input("You: ")

def returnOutput(output):
    print("Bot:", output)

bot()