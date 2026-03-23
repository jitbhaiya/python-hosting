from flask import Flask, request, render_template
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# route storage (temporary)
routes = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        file = request.files["file"]

        if file and name:
            filepath = os.path.join(UPLOAD_FOLDER, f"{name}.py")
            file.save(filepath)

            routes[name] = filepath

            return f"✅ Link created: /{name}"

    return render_template("index.html")


@app.route("/<name>")
def run_code(name):
    if name in routes:
        filepath = routes[name]

        try:
            result = subprocess.run(
                ["python", filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout + result.stderr
        except Exception as e:
            output = str(e)

        return render_template("output.html", output=output)

    return "❌ Not Found"


if __name__ == "__main__":
    app.run(debug=True)