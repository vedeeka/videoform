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

        "Simplify the code, avoid advanced animations",
        "Use only Circle, Square, or Text from Manim",
        "Ensure the Scene has a construct() method",
        "Avoid unnecessary imports and complex features"
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
    
    # Handle both string and object inputs
    if isinstance(data, str):
        original_prompt =   f"Generate only the Python Manim code (no explanations, no theory, no extra text) "
        f"that creates a long, smooth animation illustrating a {data}. "
        f"Arrange all shapes and labels so that no animation or text overlaps. "
        f"Use only direct Manim color constants (e.g., RED, BLUE, GREEN, YELLOW) without unnecessary keyword arguments. "
        f"Include continuous and sequential animations for push and pop operations so that the video lasts at least 60 seconds, "
        f"keeping the animation visible until the end. "
        f"Apply multiple, engaging animation effects (like scaling, rotating, moving, and highlighting) for each component. "
        f"Ensure the code is fully ready to run without crashing, must be at least 150 lines long, "
        f"and must return exactly the expected number of objects to avoid unpacking errors. "
        f"Do not include any explanations, comments, or text outside the code—only output the code. "
        f"Add this code snippet every single time:\n\n"
       
    else:
        prompt_text = data.get('prompt', '')
        original_prompt = f"Generate only the Python Manim code (no explanations, no theory, no extra text) that creates a long, smooth animation illustrating a {prompt_text}. Arrange all shapes and labels so that no animation or text overlaps. Use only direct Manim color constants (e.g., RED, BLUE, GREEN, YELLOW) without unnecessary keyword arguments. Include continuous and sequential animations for push and pop operations so that the video lasts at least 60 seconds, keeping the animation visible until the end. Apply multiple, engaging animation effects (like scaling, rotating, moving, and highlighting) for each component. Ensure the code is fully ready to run without crashing, must be at least 150 lines long, and must return exactly the expected number of objects to avoid unpacking errors. Do not include any explanations, comments, or text outside the code—only output the code."
    
    max_retries = data.get('max_retries', 10) if isinstance(data, dict) else 10

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
            audio_snippet = (
                
                "     audio_url = 'https://murf.ai/user-upload/one-day-temp/6f560957-b7f4-4d0f-b149-eea0687d60ff.wav'\n"
                "     audio_file = 'temp_audio.mp3'\n"
                "     r = requests.get(audio_url)\n"
                "     with open(audio_file, 'wb') as f:\n"
                "     f.write(r.content)\n"
                "     self.add_sound(audio_file)\n"
)
            import_snippet = (
                "import requests\n"
            )
            # Auto-fix common manim_voiceover mistake
            manim_code = manim_code.replace(
                "from manim_voiceover import Voiceover",
                "from manim_voiceover import VoiceoverScene\nfrom manim_voiceover.services.gtts import GTTSService"
            )

            manim_code = re.sub(
                r"(from manim import \*)",
                r"\1\n" + import_snippet,  # no indentation here
                manim_code,
                count=1
)
            manim_code = re.sub(
                r"(def construct\(self\):)",
                r"\1\n    " + audio_snippet.replace("\n", "\n    "),
                manim_code,
                count=1
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
