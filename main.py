from fastapi import FastAPI, Request, Body
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse, FileResponse
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import random
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
import markdown
from html_sanitizer import Sanitizer
sanitizer = Sanitizer()

def convert_markdown_to_html_sanitised(md):
    return sanitizer.sanitize(markdown.markdown(md))

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("are we on Deta?")


app = FastAPI()

app.mount("/svelte", StaticFiles(directory="svelte/public", html=True), name="svelte")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.environ.get("OPENAI_API_KEY")  # vars['image']#os.getenv("OPENAI_API_KEY")

client = OpenAI(
    # organization='org-Ni5AudxFddc7HLBS5Ezx4bo3',
    api_key=api_key
)
client.models.list()


@app.get("/sponge")
def sponge():
    return "sponge"


@app.get('/fake_chat')
def fake_chat():


    threads = ['thread_24kiAnZO6Pr3Z4TVsoN7ungo', 'thread_qafhq2MZvE7CWr0mzvPySbHC', 'thread_xYArecO5KymuXGnBwZY0FTXP']

    # thread_xYArecO5KymuXGnBwZY0FTXP

    messages = client.beta.threads.messages.list(
        thread_id='thread_qafhq2MZvE7CWr0mzvPySbHC'
    )

    return_messages = []

    for message in messages.data:
        msg_dict = {'role': message.role, 'message': convert_markdown_to_html_sanitised(message.content[0].text.value)}
        return_messages.append(msg_dict)

    return return_messages[:10][::-1]

class UserInput(BaseModel):
    question:str = "Please explain something from the documents to me"
    role:str='user'
@app.post('/ask_question')
async def ask_question(user_input:UserInput):
    question = user_input.question
    user = user_input.role
    print(user_input)

    answer = get_answer(question)
    return answer

def get_answer(question):
    import time

    thread_id = 'thread_qafhq2MZvE7CWr0mzvPySbHC'  # 'thread_qafhq2MZvE7CWr0mzvPySbHC'
    assistant_id = 'asst_tssjRlVs7V4kNrWLBxhzYNPo'

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        # instructions="Please address the user as Jane Doe. The user has a premium account."
    )

    outcome = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )

    while outcome.status not in  ['completed','failed']:
        print(outcome.status)

        print(f'waiting for reply from Assistant, status is: {outcome.status}')
        time.sleep(.5)
        outcome = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    print(outcome.status)
    if outcome.status == 'failed':
        return {'role': 'local system', 'message': 'it looks like the run failed. Possibly no more credits!'}

    print('Received a reply!')

    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    return_messages = []

    for message in messages.data:
        msg_dict = {'role': message.role, 'message': convert_markdown_to_html_sanitised(message.content[0].text.value)}
        return_messages.append(msg_dict)

    return return_messages[0]


@app.get("/{full_path:path}")
def render_svelte(request: Request, full_path: str):
    return FileResponse("svelte/public/index.html")




# # Press the green button in the gutter to run the script.
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
