from flask import Flask, request, send_file, render_template
import yt_dlp
import os
import uuid
import threading
import time

# 🔥 Render friendly setup
app = Flask(__name__, static_folder="static", template_folder="templates")

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


# 🔥 Health check route (IMPORTANT for UptimeRobot)
@app.route("/ping")
def ping():
    return "OK", 200


# 🔥 Auto delete function
def delete_file(path):
    time.sleep(60)
    if os.path.exists(path):
        os.remove(path)


# 🔹 Preview page
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


# 🔹 Download route
@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    quality = request.form.get("quality")

    unique_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_FOLDER}/{unique_id}.mp4"

    # 🎯 Quality control
    if quality == "best":
        format_type = "best[height<=1080][ext=mp4]/best"
    else:
        format_type = "best[height<=720][ext=mp4]/best"

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

        # 🔥 Auto delete thread
        threading.Thread(target=delete_file, args=(output_path,)).start()

        return send_file(output_path, as_attachment=True)

    except Exception:
        return render_template("index.html", error="Download failed!")


# 🔥 Render production run (IMPORTANT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
