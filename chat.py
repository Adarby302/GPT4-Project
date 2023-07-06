import json

import openai
import creds
import time
import re

import promptmaker

openai.api_key = creds.OPENAI_API_KEY
conversation = []
history = {"history": conversation}

mode = 0
total_characters = 0
chat = ""
chat_now = ""
chat_prev = ""
name = ""
grade = ""


def baseCaseTry():
    global chat_now
    global name
    global grade

    name = input("Enter your name: ")
    grade = input("Enter what grade you are in: ")
    chat_now = input("Enter A question: ")

    print("name: ", name, '\n', "Grade: ", grade, "Question: ", chat_now)

    result = name  + " said " + chat_now

    conversation.append({'role': 'user', 'content': result})
    openAIanswer()


def openAIanswer():
    global total_characters, conversation

    total_characters = sum(len(d['content']) for d in conversation)

    while total_characters > 500:
        try:
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)

        except Exception as e:
            print("Error removing old messages")

    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)
    prompt = promptmaker.getPrompt()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= prompt,
        max_tokens=128,
        temperature=1,
        top_p=0.9
    )
    message = response['choices'][0]['message']['content']
    conversation.append({'role': 'user', 'content': message})

    print(message)


baseCaseTry()
