from uvicorn import run
from fastapi import FastAPI
from wolframalpha import Client

app = FastAPI()
client = Client("4HLKUJ-762HXRP6PL")

@app.get("/")
def main(query: str):

    if 'capital of india' in query or 'capital of in' in query or 'india capital' in query or 'in capital' in query:
        return "New Delhi, Delhi, India"

    elif 'capital of bangladesh' in query or 'capital of bn' in query or 'bangladesh capital' in query or 'bn capital' in query:
        return "Dhaka, Bangladesh"

    elif 'capital of united kingdom' in query or 'capital of uk' in query or 'uk capital' in query or 'united kingdom capital' in query:
        return "London, Greater London, United Kingdom"

    elif 'capital of france' in query or 'capital of fr' in query or 'france capital' in query or 'fr capital' in query:
        return "Paris, Ile-de-France, France"

    elif 'capital of china' in query or 'capital of cn' in query or 'china capital' in query or 'cn capital' in query:
        return "Beijing, China"

    elif 'capital of usa' in query or 'capital of united states of america' in query or 'capital of us' in query or 'capital of united states of america' in query or 'usa capital' in query or 'us capital' in query:
        return "Washington, District of Columbia, United States"

    elif 'capital of japan' in query or 'capital of jp' in query or 'japan capital' in query or 'jp capital' in query or 'capital japan' in query:
        return "Tokyo, Japan"

    res = client.query(query)
    res = next(res.results).text
    return res

if __name__ == '__main__':
    run("server:app", port=8000)
