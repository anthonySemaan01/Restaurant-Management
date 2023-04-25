import openai
import os
import data.credentials as credentials

openai.api_key = credentials.gpt_api_key


def start_inference(review_comment: str):
    potential_answers = ["positive", "negative", "neutral"]
    entries = ["food", "service", "location", "price", "ambiance"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You must do multilabel classification in regards to whether the text talks positively (1), "
                        "negatively (-1), neutral (0) about price, food, service, ambiance, or location. "
                        "Response should be in JSON and follows this format: {food: 1, price: -1}. Include all "
                        "categories along with their respective value. Dont add "
                        "text to the reply, only provide the JSON"},
            {"role": "user", "content": review_comment},
        ]
    )

    return response['choices'][0]['message']['content']
