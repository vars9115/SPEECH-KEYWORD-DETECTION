from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

# Keywords to detect
KEYWORDS = [
    "python",
    "java",
    "college",
    "exam",
    "project",
    "attendance",
    "computer",
    "student"
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect_keyword():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("Listening...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)

        # Convert speech to text
        text = recognizer.recognize_google(audio)

        # Convert to lowercase
        text_lower = text.lower()

        # Detect keywords
        detected = [
            keyword for keyword in KEYWORDS
            if keyword in text_lower
        ]

        return jsonify({
            "success": True,
            "text": text,
            "keywords": detected
        })

    except sr.WaitTimeoutError:
        return jsonify({
            "success": False,
            "message": "No speech detected. Please try again."
        })

    except sr.UnknownValueError:
        return jsonify({
            "success": False,
            "message": "Could not understand the speech."
        })

    except sr.RequestError:
        return jsonify({
            "success": False,
            "message": "Speech recognition service is unavailable."
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)