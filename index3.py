import requests
import json
import langid

# Read the keyword_numbers.json file
with open('keyword_numbers.json', 'r') as file:
    keyword_numbers = json.load(file)

def detect_language(text):
    # Detect the language of the text
    lang, confidence = langid.classify(text)

    return lang, confidence

result = []

# Loop through the IDs and make GET requests
for keyword, ids in keyword_numbers.items():
    keyword_data = {"keyword": keyword, "data": []}
    for id in ids:
        url = f"https://cdn.syndication.twimg.com/tweet-result?id={id}&lang=en"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            tweet_data = {
                "context_annotations": {
                    "hashtags": [],
                    "user_mentions": []
                },
                "created_at": data["created_at"],
                "entities": [],
                "lang": "",
                "public_metrics": {
                    "likes": ""
                },
                "text": data["text"]
            }

            # Extract hashtags
            hashtags = data["entities"]["hashtags"]
            for hashtag in hashtags:
                tweet_data["context_annotations"]["hashtags"].append(hashtag["text"])

            # Extract user mentions
            user_mentions = data["entities"]["user_mentions"]
            for user in user_mentions:
                tweet_data["context_annotations"]["user_mentions"].append(user["name"])

            # Extract media URLs
            # entities = data["entities"]["media"]
            # for media in entities:
            #     tweet_data["entities"].append(media["media_url_https"])

            # Detect language
            lang, confidence = detect_language(tweet_data["text"])
            tweet_data["lang"] = lang

            # Extract likes
            tweet_data["public_metrics"]["likes"] = data["favorite_count"]

            keyword_data["data"].append(tweet_data)

        else:
            print(f"Request for ID {id} failed with status code:", response.status_code)

    result.append(keyword_data)

# Write the result to a JSON file
with open('tweet_data.json', 'w') as file:
    json.dump(result, file, indent=4)

print("Data written to tweet_data.json")