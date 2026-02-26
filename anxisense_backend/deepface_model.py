from flask import Flask, request, jsonify
from deepface import DeepFace
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------------
# Anxiety score calculation
# ----------------------------
def calculate_anxiety(emotions):
    fear = float(emotions.get("fear", 0))
    sad = float(emotions.get("sad", 0))
    surprise = float(emotions.get("surprise", 0))

    anxiety_score = (
        0.5 * fear +
        0.3 * sad +
        0.2 * surprise
    )

    if anxiety_score < 30:
        level = "Low"
    elif anxiety_score < 60:
        level = "Moderate"
    else:
        level = "High"

    return round(anxiety_score, 2), level


# ----------------------------
# API endpoint
# ----------------------------
@app.route("/analyze", methods=["POST"])
def analyze_face():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]

    filename = f"{datetime.now().timestamp()}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(filepath)

    try:
        result = DeepFace.analyze(
            img_path=filepath,
            actions=["emotion"],
            enforce_detection=False
        )

        emotions_raw = result[0]["emotion"]

        # ✅ Convert numpy floats → python floats
        emotions = {k: float(v) for k, v in emotions_raw.items()}

        dominant_emotion = result[0]["dominant_emotion"]

        anxiety_score, anxiety_level = calculate_anxiety(emotions)

        response = {
            "dominant_emotion": dominant_emotion,
            "emotion_probabilities": emotions,
            "anxiety_score": anxiety_score,
            "anxiety_level": anxiety_level
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
