### **Flask Video Streaming with HLS Conversion using FFmpeg**  

This project allows users to upload videos, convert them to HLS format using FFmpeg, and stream them using Flask.

---

## **🚀 Features**
- Upload video files via Flask API.
- Convert uploaded videos into HLS format (`.m3u8` playlists).
- Stream videos using HTTP Live Streaming (HLS).
- Debugging and logging included.

---

## **🛠 Requirements**
Make sure you have the following installed:
- Python (>= 3.10)
- Flask
- Flask-CORS
- FFmpeg (installed & added to system PATH)

### **🔧 Install Dependencies**
```sh
pip install flask flask-cors
```

---

## **📂 Project Structure**
```
/flask_video_streaming
│── /videos                 # Stores uploaded video files
│── /hls                    # Stores HLS-converted video files
│── app.py                  # Main Flask application
│── routes.py               # Handles file uploads & processing
│── process_video.py        # FFmpeg conversion logic
│── templates/index.html    # Frontend (if applicable)
│── README.md               # Project documentation
```

---

## **▶️ How to Run the Project**
### **1️⃣ Install FFmpeg**
Make sure FFmpeg is installed and accessible via command line.  
Test it using:
```sh
ffmpeg -version
```
If it's not recognized, download it from [FFmpeg Official Website](https://ffmpeg.org/download.html) and add it to your system's PATH.

### **2️⃣ Run Flask Server**
```sh
python app.py
```
The app will start on:
```
http://127.0.0.1:5000
```

---

## **📤 API Endpoints**
### **1️⃣ Upload Video**
- **Endpoint:** `/upload`
- **Method:** `POST`
- **Payload:** `multipart/form-data`  
  - **Parameter:** `file` (video file)

#### **Example using Postman or cURL**
```sh
curl -X POST -F "file=@path/to/video.mp4" http://127.0.0.1:5000/upload
```

### **2️⃣ Stream Video**
- **Endpoint:** `/hls/<filename>.m3u8`
- **Method:** `GET`
- **Example URL:**  
  ```
  http://127.0.0.1:5000/hls/upload.m3u8
  ```

---

## **⚙️ Backend Logic**
### **File Upload (`routes.py`)**
```python
from flask import Flask, request, jsonify
import os
from process_video import process_video_to_hls

app = Flask(__name__)
UPLOAD_FOLDER = "videos"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Process video using FFmpeg
    hls_url = process_video_to_hls(file_path)

    return jsonify({"hls_url": hls_url})

if __name__ == "__main__":
    app.run(debug=True)
```

---

### **FFmpeg Processing (`process_video.py`)**
```python
import subprocess
import os

HLS_FOLDER = "hls"

if not os.path.exists(HLS_FOLDER):
    os.makedirs(HLS_FOLDER)

def process_video_to_hls(file_path):
    filename = os.path.basename(file_path)
    output_file = os.path.join(HLS_FOLDER, f"{filename}.m3u8")

    ffmpeg_cmd = f'ffmpeg -i "{file_path}" -codec copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{output_file}"'
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

    return f"/hls/{filename}.m3u8"
```

---

## **🔥 Troubleshooting**
### **1️⃣ FFmpeg is not recognized?**
- Add FFmpeg to your system's PATH and restart the terminal.
- Test with:
  ```sh
  ffmpeg -version
  ```

### **2️⃣ "File Not Found" Error?**
- Ensure the uploaded file is saved in the `/videos` directory.
- Run:
  ```sh
  dir videos
  ```
- If missing, move it manually or check your upload logic.

### **3️⃣ Permission Denied for FFmpeg?**
- Run the command with admin privileges.

---

## **📜 License**
This project is open-source and available under the MIT License.

---

## **🙌 Contributing**
Feel free to fork this project and submit a pull request! 🚀