from openai import OpenAI
import os
import subprocess
from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import re
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

client = OpenAI(api_key="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")


def extract_scene_name(code: str) -> str:
    """Find first Scene subclass in the generated code"""
    match = re.search(r"class\s+(\w+)\(Scene\):", code)
    return match.group(1) if match else None
@app.route('/generate_manim_code', methods=['POST'])
def generate_manim_code():
    data = request.json
    prompt = data.get('prompt', data)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    manim_code = response.choices[0].message.content.strip()
    # remove markdown fences if present
    if manim_code.startswith("```"):
        manim_code = manim_code.split("```")[1].replace("python", "").strip()

    file_path = "generated_manim.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(manim_code)
    os.system("manim -pql generated_manim.py GeneratedScene")
    # auto-detect Scene class name
    scene_name = extract_scene_name(manim_code) or "Scene"

    try:
        run_output = subprocess.run(
            ["manim", "-pql", file_path, scene_name],
            capture_output=True,
            text=True,
            check=True
        )
        result = run_output.stdout
        success = True
    except subprocess.CalledProcessError as e:
        result = e.stderr
        success = False
    except FileNotFoundError:
        result = "❌ 'manim' command not found. Try running inside the same venv where Manim is installed."
        success = False

    return jsonify({
        "file_path": os.path.abspath(file_path),
        "scene_name": scene_name,
        "success": success,
        "manim_output": result
    })

if __name__ == '__main__':
    app.run(debug=True)
