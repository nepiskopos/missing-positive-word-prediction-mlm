from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse

try:
    from predict import init_models, validate_text, predict_words, remove_negative_sentiment
except ImportError:
    from .predict import init_models, validate_text, predict_words, remove_negative_sentiment



# Initialize prediction models and relevant parameters
init_models()

# Define a new FastAPI app
app = FastAPI()


# Define the behaviour of a POST request to the root of the server
@app.post('/api/predict_single', tags=['predict a single masked word using bert mlm'])
async def predict_text(response: JSONResponse, input_text: str=Body(...)):
    '''
    Predict a single missing word in a sentence, masked under the <blank>
    keyword, which is given to the API as an input string. The predicted
    missing words always give a positive sentiment to the input sentence.

    **Input**: Raw string using the data ("body") part of the HTTP POST request.

    **Returns**: A JSON file which contains a list of strings which satisfy the
                 positive sentiment requirements under the "content" name (key)
                 or with a suitable error message in case an error occurs, or if
                 the input sentence does not contain the <blank> keyword or if
                 no suitable words are predicted. If more than one <blank>
                 keywords exist in the input string, word predictions will be
                 performed only for the first <blank> occurence.

    **Example**:
        - Input: "I wish you have a &lt;blank&gt; day!"
        - Return JSON: {"content": ["good","free","nice","better","perfect","great"]}

    **API test using cURL**:\n
        curl -X 'POST' 'http://API_IP_ADDRESS:PORT/predict'
             -H 'accept: application/json'
             -H 'Content-Type: text/plain'
             -d 'I wish you have a &lt;blank&gt; day!'
    '''
    response_content = None
    response_status = None

    if not validate_text(input_text):
        response_content = 'Wrong input'
        response_status = status.HTTP_422_UNPROCESSABLE_ENTITY

    if not response_content:
        predicted_words = predict_words(input_text)

        if not predict_words:
            response_content = 'No suitable words'
            response_status = status.HTTP_200_OK

    if not response_content:
        acceptable_words = remove_negative_sentiment(input_text, predicted_words)

        if not acceptable_words:
            response_content = 'No suitable words'
        else:
            response_content = acceptable_words

        response_status = status.HTTP_200_OK

    return JSONResponse(content={"content": response_content}, status_code=response_status)
