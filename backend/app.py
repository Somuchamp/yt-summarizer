# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import pipeline

# # Initialize local summarizer
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# app = Flask(__name__)
# CORS(app)

# def extract_video_id(url):
#     if "v=" in url:
#         return url.split("v=")[1].split("&")[0]
#     elif "youtu.be/" in url:
#         return url.split("youtu.be/")[1].split("?")[0]
#     else:
#         return None

# @app.route("/summarize", methods=["POST"])
# def summarize():
#     try:
#         data = request.get_json()
#         url = data.get("url")
#         video_id = extract_video_id(url)

#         if not video_id:
#             return jsonify({"error": "Invalid YouTube URL"}), 400

#         # Get transcript
#         transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = " ".join([entry['text'] for entry in transcript_data])

#         # BART limit: truncate if too long
#         text_to_summarize = transcript[:1024]

#         # Run local model
#         summary = summarizer(text_to_summarize, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

#         return jsonify({"summary": summary})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from transformers import pipeline

# Initialize local summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

app = Flask(__name__)
CORS(app)

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        url = data.get("url")
        video_id = extract_video_id(url)

        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        try:
            # Try to fetch English transcript
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except (TranscriptsDisabled, NoTranscriptFound):
            try:
                # Fallback: fetch any available transcript
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_transcript(
                    [t.language_code for t in transcript_list]
                )
                transcript_data = transcript.fetch()
            except Exception as fallback_err:
                return jsonify({"error": "No usable transcript found (English or otherwise)."}), 404

        # Join transcript lines
        transcript = " ".join([entry['text'] for entry in transcript_data])

        # Truncate if too long for BART model
        text_to_summarize = transcript[:1024]

        # Run local model
        summary = summarizer(text_to_summarize, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
