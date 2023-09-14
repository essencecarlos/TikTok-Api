from flask import Flask, request
from typing import List, Dict
from tiktokapipy.async_api import AsyncTikTokAPI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import asyncio
import os
import json
 
app = Flask(__name__)
# video_url = "https://www.tiktok.com/@_flossinator_/video/7263234408734395680"
ms_token = os.environ.get("ms_token", None)  # set your own ms_token
 
@app.route('/crawl')
async def index():
    # Get the value of the 'name' parameter from the URL
    post = request.args.get('post')
    sentences = [];
    sentiments = [];
    
    async with AsyncTikTokAPI() as api:
        
        video = await api.video(post)
        print(video.comments)
        
        async for comment in video.comments.limit(70):
            # print(comment.text)
            sentences.append(comment.text)
        if len(sentences) > 0 :
            analyzer = SentimentIntensityAnalyzer()
            for sentence in sentences:
                vs = analyzer.polarity_scores(sentence)
                sentiments.append([sentence, vs]);
                print("{:-<65} {}".format(sentence, str(vs)))
        else : print("no sentences!")

    return json.dumps(sentiments);

if __name__ == "__main__": 
    app.run()