from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from pathlib import Path
from uuid import uuid4
from datetime import datetime
from itertools import combinations
from openpyxl import Workbook
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me")

BASE_DIR = Path(__file__).resolve().parent
WAV_DIR = BASE_DIR.parent / "ExSystem03_wav"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".wav"}

sessions = {}


def get_wav_files():
    if not WAV_DIR.exists() or not WAV_DIR.is_dir():
        return []
    files = [f for f in sorted(WAV_DIR.iterdir())
             if f.suffix.lower() in ALLOWED_EXTENSIONS]
    return files


def build_pairs(file_list):
    names = [f.name for f in sorted(file_list)]
    pairs = list(combinations(names, 2))
    random.shuffle(pairs)
    return pairs


def create_result_file(participant_name, results):
    safe_name = "_".join(participant_name.strip().split()) or "participant"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp}.xlsx"
    path = RESULTS_DIR / filename

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "results"
    sheet.append(["File A", "File B", "Rating", "Trial Order",
                 "Play Count A", "Play Count B", "Response Time"])

    for row in results:
        sheet.append([
            Path(row["file_a"]).stem,
            Path(row["file_b"]).stem,
            row["rating"],
            row["trial_order"],
            row["play_count_a"],
            row["play_count_b"],
            row["response_time"],
        ])

    workbook.save(path)
    return filename


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("氏名を入力してください。", "warning")
            return redirect(url_for("index"))

        wav_files = get_wav_files()
        if not wav_files:
            flash("WAVファイルが見つかりません。ExSystem03と同階層のExSystem03_wavフォルダを確認してください。", "danger")
            return redirect(url_for("index"))

        pairs = build_pairs(wav_files)
        if not pairs:
            flash("WAVファイルが2つ以上必要です。", "danger")
            return redirect(url_for("index"))

        session_id = str(uuid4())
        sessions[session_id] = {
            "name": name,
            "pairs": pairs,
            "current": 0,
            "results": [],
            "counts": {p.name: 0 for p in wav_files},
            "created_at": datetime.now(),
        }
        session["session_id"] = session_id
        return redirect(url_for("experiment", session_id=session_id))

    return render_template("index.html")


@app.route("/experiment/<session_id>")
def experiment(session_id):
    session_data = sessions.get(session_id)
    if not session_data:
        flash("セッションが見つかりません。もう一度開始してください。", "danger")
        return redirect(url_for("index"))

    current = session_data["current"]
    pairs = session_data["pairs"]
    if current >= len(pairs):
        return redirect(url_for("complete", session_id=session_id))

    file_a, file_b = pairs[current]
    return render_template(
        "experiment.html",
        name=session_data["name"],
        file_a=file_a,
        file_b=file_b,
        trial=current + 1,
        total=len(pairs),
        session_id=session_id,
    )


@app.route("/submit/<session_id>", methods=["POST"])
def submit(session_id):
    session_data = sessions.get(session_id)
    if not session_data:
        flash("セッションが見つかりません。", "danger")
        return redirect(url_for("index"))

    rating = request.form.get("rating")
    if rating not in [str(i) for i in range(1, 8)]:
        flash("1から7までの評価を選択してください。", "warning")
        return redirect(url_for("experiment", session_id=session_id))

    current = session_data["current"]
    file_a, file_b = session_data["pairs"][current]
    session_data["results"].append({
        "file_a": file_a,
        "file_b": file_b,
        "rating": int(rating),
        "trial_order": current + 1,
        "play_count_a": session_data["counts"].get(file_a, 0),
        "play_count_b": session_data["counts"].get(file_b, 0),
        "response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    session_data["current"] += 1
    return redirect(url_for("experiment", session_id=session_id))


@app.route("/abort/<session_id>", methods=["POST"])
def abort(session_id):
    session_data = sessions.get(session_id)
    if not session_data:
        flash("セッションが見つかりません。", "danger")
        return redirect(url_for("index"))

    filename = create_result_file(
        session_data["name"], session_data["results"])
    return render_template(
        "complete.html",
        name=session_data["name"],
        filename=filename,
        aborted=True,
    )


@app.route("/complete/<session_id>")
def complete(session_id):
    session_data = sessions.get(session_id)
    if not session_data:
        flash("セッションが見つかりません。", "danger")
        return redirect(url_for("index"))

    if not session_data["results"]:
        flash("結果がありません。", "warning")
        return redirect(url_for("index"))

    filename = create_result_file(
        session_data["name"], session_data["results"])
    return render_template(
        "complete.html",
        name=session_data["name"],
        filename=filename,
    )


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(RESULTS_DIR, filename, as_attachment=True)


@app.route("/wav/<path:filename>")
def serve_wav(filename):
    return send_from_directory(WAV_DIR, filename)


@app.route("/count_play/<session_id>", methods=["POST"])
def count_play(session_id):
    session_data = sessions.get(session_id)
    if not session_data:
        return ("", 404)
    filename = request.json.get("filename")
    if filename in session_data["counts"]:
        session_data["counts"][filename] += 1
    return ("", 204)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
