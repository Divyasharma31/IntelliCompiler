

import urllib.request
import urllib.error
import json
import os

key = os.environ.get("GROQ_API_KEY", "")

if not key:
    print("Please set GROQ_API_KEY environment variable")
    print("Get your key from: https://console.groq.com")
    exit(1)

payload = json.dumps({
    "model": "llama3-8b-8192",
    "messages": [{"role": "user", "content": "Say hello in one word."}],
    "max_tokens": 10
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.groq.com/openai/v1/chat/completions",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("SUCCESS:", data["choices"][0]["message"]["content"])
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print(e.read().decode("utf-8"))
except Exception as e:
    print("Error:", e)