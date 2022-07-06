import pandas as pd
import re
import json
import unknown

def load_json(file):
    with open(file) as openedFile:
        return json.load(openedFile)

#symptoms = pd.DataFrame(columns = ["Symptom", "Probing question", "Diseases"]);
#diseases = pd.DataFrame(columns = ["Disease", "Symptoms", "Time Period", "Treatment"]);


symptoms = load_json("symptoms.json")
diseases = load_json("diseases.json")
greetResponses = load_json("greet.json")
responses = load_json("response_data.json")


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
    greeting_statement = "Hello! Welcome to Apollo Hospitals. How are you feeling today?"
    ending_statement = "Can I help you in any other way?"
    def greet():
        returnOutput(greeting_statement)
        returnOutput(processInput(input = getInput(), response_data = greetResponses)["response"])
        diagnose(processInput(input=getInput(), response_data= symptoms))

    #diagnosis 1
    def diagnose(symptom):
        #make a list of diseases with that symptom
        possible_diseases = diseases
        #make a priority list of symptoms that we need to rule out with priority bring how close it is to 50%
        possible_symptoms = {}

        confirmed_symptoms = []

        def add_symptom(symptom):
            nonlocal possible_symptoms
            nonlocal possible_diseases
            if symptom["name"] in possible_symptoms:
                possible_symptoms[symptom["name"]] = (symptom, possible_symptoms[symptom["name"]][1] + 1)
            else:
                possible_symptoms[symptom["name"]] = (symptom, 1)
            possible_symptoms = {k: v for k, v in sorted(possible_symptoms.items(), reverse=True, key=lambda item: item[1][1])}

        def confirm_symptom(symptom):
            nonlocal possible_symptoms
            nonlocal possible_diseases
            nonlocal confirmed_symptoms
            possible_symptoms = {}
            new_possible_diseases = []
            confirmed_symptoms.append(symptom)
            for disease in possible_diseases:
                if symptom["name"] in disease["symptoms"]:
                    new_possible_diseases.append(disease)
                    for new_symptom_name in disease["symptoms"]:
                        if new_symptom_name in confirmed_symptoms:
                            continue
                        for symptom_data in symptoms:
                            if symptom_data["name"] == new_symptom_name:
                                add_symptom(symptom_data)

            possible_diseases = new_possible_diseases
        
        def remove_symptom(symptom):
            nonlocal possible_symptoms
            nonlocal possible_diseases
            nonlocal confirmed_symptoms
            possible_symptoms = {}
            new_possible_diseases = []
            confirmed_symptoms.append(symptom)
            for disease in possible_diseases:
                if symptom["name"] not in disease["symptoms"]:
                    new_possible_diseases.append(disease)
                    for new_symptom_name in disease["symptoms"]:
                        if new_symptom_name in confirmed_symptoms:
                            continue
                        for symptom_data in symptoms:
                            if symptom_data["name"] == new_symptom_name:
                                add_symptom(symptom_data)

            possible_diseases = new_possible_diseases

        confirm_symptom(symptom)

        keys = list(possible_symptoms.keys())
        while(len(possible_diseases) > 1 and possible_symptoms[keys[0]][1] != possible_symptoms[keys[-1]][1]):
            next_symptom = possible_symptoms.popitem()[1][0]
            returnOutput(next_symptom["probing question"])
            if (processInput(getInput(), responses)["intent"] == "YES"):
                confirm_symptom(next_symptom)
            else:
                remove_symptom(next_symptom)

        if len(possible_diseases) < 1:
            returnOutput("No such disease found")
        else:
            returnOutput(possible_diseases.pop()["treatment"])
            ending()
    #treatment 2

    #ending 3
    def ending():
        returnOutput(ending_statement)
        if (processInput(input = getInput(), response_data = responses)["intent"] == "YES"):
            greet()
        else:
            returnOutput("Thank you for using our services. Please provide us with valuable feedback at www.feedback.com")

    greet()
    


def getInput(): 
    return input("You: ")

def returnOutput(output):
    print("Bot:", output)

bot()
