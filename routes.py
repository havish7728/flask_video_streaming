from flask import request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from app import app, db
from models import Video
from process_video import process_video_to_hls

@app.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["video"]
    title = request.form.get("title", "Untitled")
    filename = secure_filename(file.filename)

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    hls_url = process_video_to_hls(file_path)

    new_video = Video(title=title, filename=filename, resolution="auto", storage_url=hls_url)
    db.session.add(new_video)
    db.session.commit()

    return jsonify({"message": "Video uploaded successfully", "hls_url": hls_url})

@app.route("/hls/<path:filename>")
def stream_video(filename):
    return send_from_directory(app.config["HLS_FOLDER"], filename)
