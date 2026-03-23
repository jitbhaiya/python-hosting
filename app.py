from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

routes = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        file = request.files.get("file")

        if not name or not file:
            return "❌ Name or file missing"

        # Only allow .py files
        if not file.filename.endswith(".py"):
            return "❌ Only .py files allowed"

        filepath = os.path.join(UPLOAD_FOLDER, f"{name}.py")
        file.save(filepath)

        routes[name] = filepath

        return f"✅ Link created: /{name}"

    return render_template("index.html")


@app.route("/<name>")
def run_code(name):
    if name not in routes:
        return "❌ Not Found"

    filepath = routes[name]

    try:
        result = subprocess.run(
            ["python3", filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr

    except subprocess.TimeoutExpired:
        output = "⏱️ Timeout (5 sec limit)"

    except Exception as e:
        output = str(e)

    return render_template("output.html", output=output)


# 🔥 IMPORTANT for Render (Production)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
