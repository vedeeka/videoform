import os
import re
import time
import subprocess
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

# Flask setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "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"  # fallback for dev
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_scene_name(code: str) -> str:
    """Extract the first Scene class name from the Manim code"""
    match = re.search(r"class\s+(\w+)\(\w+\):", code)
    return match.group(1) if match else None

def run_manim_with_retry(file_path: str, scene_name: str, max_retries: int = 3) -> tuple[bool, str]:
    """Run manim command and return success status and output"""
    try:
        run_output = subprocess.run(
            ["manim", "-pql", file_path, scene_name],
            capture_output=True,
            text=True,
            check=True
        )
        return True, run_output.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except FileNotFoundError:
        return False, "❌ 'manim' command not found. Make sure you're in the venv with Manim installed."

def generate_improved_prompt(original_prompt: str, error_message: str, attempt: int) -> str:
    """Generate an improved prompt for fixing broken Manim code"""
    variations = [
        "Do  use voiceover and GTTS,",
        
        "Use only Circle, Square, or Text from Manim.",
        "Ensure the Scene has a construct() method.",
        "Avoid unnecessary imports.",
    ]
    tweak = random.choice(variations)

    return f"""The previous attempt to generate Manim code failed with error: {error_message}

Original request: {original_prompt}

Please fix the code and generate a corrected version. Make sure to:
1. Fix any syntax errors
2. Ensure all imports are correct
3. Define a valid Scene class
4. Use valid Manim methods and objects
5. {tweak}

Attempt number: {attempt}

Generate corrected Manim code:"""

@app.route('/generate_manim_code', methods=['POST'])
def generate_manim_code():
    data = request.json
    original_prompt = data.get('prompt', data)
    max_retries = data.get('max_retries', 5)

    file_path = "generated_manim.py"
    current_prompt = original_prompt
    all_attempts = []

    for attempt in range(1, max_retries + 1):
        print(f"Attempt {attempt}/{max_retries}")

        try:
            # Ask Gemini for Manim code
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": current_prompt}]
            )

            manim_code = response.choices[0].message.content.strip()

            # Clean markdown fences if present
            if manim_code.startswith("```"):
                manim_code = manim_code.split("```")[1].replace("python", "").strip()

            # Auto-fix common manim_voiceover mistake
            manim_code = manim_code.replace(
                "from manim_voiceover import Voiceover",
                "from manim_voiceover import VoiceoverScene\nfrom manim_voiceover.services.gtts import GTTSService"
            )

            # Write code to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(manim_code)

            # Detect Scene class
            scene_name = extract_scene_name(manim_code) or "Scene"

            # Run with Manim
            success, result = run_manim_with_retry(file_path, scene_name)

            attempt_info = {
                "attempt": attempt,
                "success": success,
                "output": result,
                "scene_name": scene_name
            }
            all_attempts.append(attempt_info)

            if success:
                print(f"✅ Success on attempt {attempt}")
                return jsonify({
                    "file_path": os.path.abspath(file_path),
                    "scene_name": scene_name,
                    "success": True,
                    "manim_output": result,
                    "attempts": all_attempts,
                    "final_attempt": attempt
                })
            else:
                print(f"❌ Failed on attempt {attempt}: {result[:120]}...")
                # Try again with tweaked prompt
                current_prompt = generate_improved_prompt(original_prompt, result, attempt + 1)
                time.sleep(1)

        except Exception as e:
            error_msg = f"Error generating code: {str(e)}"
            print(f"❌ Error on attempt {attempt}: {error_msg}")
            all_attempts.append({
                "attempt": attempt,
                "success": False,
                "output": error_msg,
                "scene_name": None
            })
            current_prompt = generate_improved_prompt(original_prompt, error_msg, attempt + 1)
            time.sleep(1)

    print(f"❌ All {max_retries} attempts failed")
    return jsonify({
        "file_path": os.path.abspath(file_path),
        "scene_name": None,
        "success": False,
        "manim_output": f"Failed after {max_retries} attempts. Check attempts array for details.",
        "attempts": all_attempts,
        "final_attempt": max_retries
    })

if __name__ == '__main__':
    app.run(debug=True)
