import json
import os
import openai
import creds
import promptmaker
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
openai.api_key = creds.OPENAI_API_KEY
conversation = []


app.add_middleware(

    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

@app.post("/ask_question/")
async def ask_question(request: Request):
    pass

def baseCaseTry(message):
    global conversation

    name = input("Enter your name: ")
    grade = input("Enter what grade you are in: ")
    chat_now = input("Enter a question: ")

    print("Name:", name)
    print("Grade:", grade)
    print("Question:", chat_now)

    result = name + " said " + chat_now
    conversation.append({'role': 'user', 'content': result})
    openai_answer()

def openai_answer():
    global conversation
    # Remove old messages if total characters exceed 4000
    total_characters = sum(len(d['content']) for d in conversation)
    while total_characters > 4000:
        try:
            conversation.pop(0)  # Remove the oldest message
            total_characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error removing old messages:", e)

    # Read the existing conversation from the JSON file
    if os.path.isfile("conversation.json"):
        with open("conversation.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            history = existing_data.get("history", [])
    else:
        history = []

    # Append the new conversation to the existing history
    history.extend(conversation)

    # Write the updated conversation history to the JSON file
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump({"history": history}, f, indent=4)

    prompt = history  # Use conversation instead of history

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=128,
        temperature=1,
        top_p=0.9
    )
    message = response['choices'][0]['message']['content']
    assistant_response = {'role': 'assistant', 'content': message}
    conversation.append(assistant_response)
    history.append(assistant_response)  # Append to history as well

    # Write the updated conversation history to the JSON file
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump({"history": history}, f, indent=4)

    return message


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

main()