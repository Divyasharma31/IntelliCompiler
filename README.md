# 🤖 AI-Powered Mini Compiler (C++ Error Correction System)

An interactive mini compiler built in Python that performs **Lexical, Syntax, and Semantic Analysis** on C++ code and uses **AI to automatically detect and correct errors**.

---

## 🚀 Features

* 🔍 **Lexical Analysis**

  * Tokenizes C++ code
  * Detects invalid identifiers and characters

* 🧩 **Syntax Analysis**

  * Parses code structure
  * Identifies missing semicolons, incorrect statements

* 🧠 **Semantic Analysis**

  * Builds symbol table
  * Detects undeclared variables and type issues

* 🤖 **AI Error Correction**

  * Fix errors automatically using AI
  * Explains mistakes in simple terms
  * Provides corrected full C++ code

* 🎯 **Interactive Mode**

  * Choose between:

    * AI correction
    * Manual correction
    * Skipping a phase

---

## 🛠️ Tech Stack

* Python 3
* Custom Lexer, Parser, Semantic Analyzer
* OpenRouter API / Groq API (for AI correction)

---

## 📂 Project Structure

```
compiler_design_project/
│
├── main.py
├── ai_correction.py
├── lexer.py
├── parser.py
├── semantic.py
├── corrected_code.cpp
└── original_code.cpp
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/Divyasharma31/IntelliCompiler.git
cd AI-Compiler-Assistant
```

---

### 2. Install Requirements

No external libraries required (uses built-in Python modules)

---

### 3. Set API Key (IMPORTANT)

#### Option A: OpenRouter

1. Get key from: https://openrouter.ai/keys

```
export OPENROUTER_API_KEY="your_api_key_here"
```

---

#### Option B: Groq (Recommended)

1. Get key from: https://console.groq.com

```
export GROQ_API_KEY="your_api_key_here"
```

---

### 4. Run the Program

```
python3 main.py
```

---

## 🧪 Example Input (C++ with Errors)

```cpp
#include <iostream>
using namespace std;

int main() {
    intt x = 10;
    int y = 20;
    int z = x + y;
    num = "hello";
    float result = x + y
    int val = @;
    cout << z << endl;
    cout << undefined_var << endl;
    return 0;
}
```

---

## ✅ Output

* Error detection in all 3 phases
* AI-generated:

  * Explanation
  * Corrected code
  * Tips

---

## 📸 Sample Flow

1. Run program
2. Choose correction method (AI / Manual / Skip)
3. View AI suggestions
4. Apply fixes
5. Get final corrected C++ code

---

## ⚠️ Common Issues

* ❌ `API Error 401 Unauthorized`

  * You are using the wrong API key
  * Make sure you use:

    * OpenRouter → `sk-or-...`
    * Groq → valid key from console

* ❌ AI not working

  * Ensure API key is set:

    ```
    echo $OPENROUTER_API_KEY
    ```

---

## 🌟 Future Improvements

* GUI interface
* Support for more programming languages
* Real-time error highlighting
* Integration with VS Code

---

## 👨‍💻 Author

**Divya Sharma**

---

## 📄 License

This project is for educational purposes.
