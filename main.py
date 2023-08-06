from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/get_video")
def get_video():
    if request.args:
        if len(request.args.getlist('term')) == 1:
           terms = [request.args.get('term')]
        else:
            terms = request.args.getlist('term')

        videos = file_json

        for term_json in terms:
            term = json.loads(term_json)

            if term['filter'] == 'strict':
                videos = strict_search(videos,term['field'],term['text'])

            if term['filter'] == 'partial':
                videos = partial_search(videos,term['field'],term['text'])

            if term['filter'] == 'between':
                videos = between_search(videos,term['field'],term['text'])

        out = videos
        return jsonify(out), 200
    return None, 100

def strict_search(data, field, text):
    return [video for video in data if video[field] == text]

def partial_search(data, field, text):
    return [video for video in data if text in video[field]]

def between_search(data, field, text):
    text_from, text_to = text.split(",")
    return [video for video in data if str(video[field]) >= text_from and str(video[field]) <= text_to]

if __name__ == "__main__":
    file = open('videos.json')
    file_json = json.load(file)
    app.run(debug = True)