from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid
import threading
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# 🔥 Auto delete function
def delete_file(path):
    time.sleep(10)  # 10 sec pore delete
    if os.path.exists(path):
        os.remove(path)


# 🔹 Preview (lightweight)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")

        try:
            with yt_dlp.YoutubeDL({
                "quiet": True,
                "skip_download": True
            }) as ydl:
                info = ydl.extract_info(url, download=False)

            return render_template(
                "index.html",
                title=info.get("title"),
                thumbnail=info.get("thumbnail"),
                url=url
            )

        except Exception:
            return render_template("index.html", error="Invalid link!")

    return render_template("index.html")


# 🔹 ULTRA FAST DOWNLOAD (LOW QUALITY)
@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")

    unique_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_FOLDER}/{unique_id}.mp4"

    ydl_opts = {
        "outtmpl": output_path,
        "format": "worst[ext=mp4]/worst",
        "quiet": True,
        "noplaylist": True,
        "concurrent_fragment_downloads": 5
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # 🔥 AUTO DELETE START
        threading.Thread(target=delete_file, args=(output_path,)).start()

        return send_file(output_path, as_attachment=True)

    except Exception:
        return render_template("index.html", error="Download failed!")


if __name__ == "__main__":
    app.run(debug=True)