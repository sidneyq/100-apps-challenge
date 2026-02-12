# App 001: Unit Converter
# TODO: Build this with Replit AI Agent
# Prompt: "Build a Flask web app unit converter with dropdowns for
# category (temperature, distance, weight) and conversion direction.
# Number input, instant result. Clean mobile-friendly layout."

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>App 001: Unit Converter</h1><p>Coming soon...</p>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
