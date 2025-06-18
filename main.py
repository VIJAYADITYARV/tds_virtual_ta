from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from difflib import get_close_matches

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


qa_data = [
    {
        "question": "How do I install pandas in Python?",
        "answer": "You can install pandas using pip with the command: pip install pandas.",
        "url": "https://discourse.s-anand.net/t/installing-pandas"
    },
    {
        "question": "What is the difference between list and tuple in Python?",
        "answer": "Lists are mutable, whereas tuples are immutable.",
        "url": "https://discourse.s-anand.net/t/list-vs-tuple"
    },
    {
        "question": "Why is pandas slow on large CSVs?",
        "answer": "Pandas loads entire CSVs into memory. For large files, consider using chunksize or Dask.",
        "url": "https://discourse.s-anand.net/t/pandas-performance"
    },
    {
        "question": "What does the error 'KeyError' mean in Python?",
        "answer": "A KeyError occurs when a dictionary key is not found.",
        "url": "https://discourse.s-anand.net/t/python-keyerror"
    },
    {
        "question": "How do I fix module not found error in Python?",
        "answer": "Use pip install <module-name> to install the missing module.",
        "url": "https://discourse.s-anand.net/t/module-not-found-error"
    }
]

class Question(BaseModel):
    question: str
    
@app.get("/")
async def root():
    return {"message": "Virtual TA is live!"}

@app.post("/")
async def get_answer(q: Question):
    questions = [item['question'] for item in qa_data]
    match = get_close_matches(q.question, questions, n=1, cutoff=0.4)
    if match:
        for qa in qa_data:
            if qa['question'] == match[0]:
                return {
                    "answer": qa['answer'],
                    "url": qa['url']
                }
    return {
        "answer": "Sorry, I could not find a relevant answer.",
        "url": "https://discourse.s-anand.net"
    }
