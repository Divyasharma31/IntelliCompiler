

import urllib.request
import urllib.error
import json
import os
import re
from lexer import tokenize

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_api_key(provider="openrouter"):
    if provider == "openrouter":
        key = os.environ.get("OPENROUTER_API_KEY", "")
        if not key:
            print("\n[AI Module] OPENROUTER_API_KEY not set.")
        return key
    else:
        key = os.environ.get("GROQ_API_KEY", "")
        if not key:
            print("\n[AI Module] GROQ_API_KEY not set.")
        return key


def build_prompt_for_phase(source_code, errors, phase_name):
    if not errors:
        return None

    error_block = "\n".join(errors)

    return f"""
You are a C++ compiler assistant helping a beginner student.

C++ CODE:
{source_code}

ERRORS IN {phase_name.upper()} PHASE:
{error_block}

TASK:
1. Explain each error simply.
2. Provide FULL corrected C++ code (do not remove lines).
3. Give one short tip.

FORMAT:

EXPLANATION:
...

CORRECTED CODE:
<code here>

TIP:
...
"""


def call_ai_api(prompt, api_key, provider="openrouter"):
    if provider == "openrouter":
        url = OPENROUTER_URL
        payload = {
            "model": "openrouter/auto",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    else:
        url = GROQ_URL
        payload = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"API Error: {e}"


def extract_corrected_code(ai_response):
    # Try to extract code block
    pattern = r"CORRECTED CODE:\s*(.*?)(TIP:|$)"
    match = re.search(pattern, ai_response, re.DOTALL)

    if match:
        return match.group(1).strip()

    return None


def interactive_phase_correction(phase_name, source_code, errors):
    print("\n" + "=" * 50)
    print(f"{phase_name.upper()} PHASE")
    print("=" * 50)

    if not errors:
        print("No errors found.")
        return source_code

    print("Errors:")
    for e in errors:
        print("-", e)

    choice = input("\n1 = AI fix | 2 = manual | 3 = skip : ").strip()

    if choice == "3":
        return source_code

    if choice == "2":
        print("Enter corrected code (END to finish):")
        lines = []
        while True:
            line = input()
            if line == "END":
                break
            lines.append(line)
        return "\n".join(lines)

    # AI fix
    api_key = get_api_key("openrouter") or get_api_key("groq")
    if not api_key:
        print("No API key found.")
        return source_code

    prompt = build_prompt_for_phase(source_code, errors, phase_name)
    response = call_ai_api(prompt, api_key)

    print("\nAI RESPONSE:\n")
    print(response)

    code = extract_corrected_code(response)

    if code:
        print("\nApplying AI fix...")
        return code
    else:
        print("Failed to extract code.")
        return source_code


def run_ai_correction(source_code, lex_errors, syn_errors, sem_errors):
    print("\n=== AI CORRECTION SYSTEM ===\n")

    code = source_code

    code = interactive_phase_correction("lexical", code, lex_errors)
    code = interactive_phase_correction("syntax", code, syn_errors)
    code = interactive_phase_correction("semantic", code, sem_errors)

    print("\nFINAL CODE:\n")
    print(code)

    try:
        with open("corrected_code.cpp", "w") as f:
            f.write(code)
        print("\nSaved to corrected_code.cpp")
    except Exception as e:
        print("Save error:", e)