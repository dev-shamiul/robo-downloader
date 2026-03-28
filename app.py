from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid
import threading
import time

# 🔥 IMPORTANT (static + templates fix)
app = Flask(__name__, static_folder="static", template_folder="templates")

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# 🔥 Auto delete function (time increase)
def delete_file(path):
    time.sleep(60)  # 1 min pore delete
    if os.path.exists(path):
        os.remove(path)


# 🔹 Preview (lightweight)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        quality = request.form.get("quality")

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
                url=url,
                quality=quality
            )

        except Exception:
            return render_template("index.html", error="Invalid link!")

    return render_template("index.html")


# 🔹 DOWNLOAD (QUALITY SUPPORT ADDED)
@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    quality = request.form.get("quality")

    unique_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_FOLDER}/{unique_id}.mp4"

    # 🎯 Quality control
    if quality == "best":
        format_type = "best[ext=mp4]/best"
    else:
        format_type = "worst[ext=mp4]/worst"

    ydl_opts = {
        "outtmpl": output_path,
        "format": format_type,
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


# ❌ debug remove (Render friendly)
if __name__ == "__main__":
    app.run()
