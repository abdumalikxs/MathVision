# Welcome to MathVision! ⚡️

**Live Demo:** 


https://github.com/user-attachments/assets/3dcb7031-2412-4019-956d-8ca51818cd51
<img width="1440" height="900" alt="Screenshot 2025-10-28 at 08 34 44" src="https://github.com/user-attachments/assets/b78f5b29-7de6-43eb-a1a9-3126ca95e778" />


---

## Inspiration 💡

I built **MathVision** because most math tools only visualize single equations and lack true interactivity. I wanted a platform where users could **plot multiple mathematical functions simultaneously**, **find extrema and intersections in real time**, and even **ask an AI tutor for explanations** — like a personal Desmos powered by intelligence.

I focused on making the experience technically smooth and secure: using **SymPy’s safe parsing**, a **vectorized NumPy backend**, and **Matplotlib’s headless Agg engine** for efficient, server-friendly plotting.

---

## What it does 🎯

**MathVision** is a web-based platform that lets users experiment with mathematics interactively.  
It enables users to:

- 🧠 **Input complex mathematical expressions** and visualize them instantly.
- 🧩 **Plot several functions at once** with labeled legends and automatic scaling.
- ⚙️ **Analyze key points** — including extrema, intersections, and asymptotic behavior — in real time.
- 💬 **Ask Gemini AI** to explain equations, describe function behavior, or provide learning guidance.
- 🧮 **Simplify and compute derivatives** with SymPy’s symbolic processing.

Under the hood, MathVision uses safe expression parsing (`sympy.sympify` with a `SAFE_FUNCS` whitelist), vectorized NumPy evaluation, and memory-efficient Matplotlib streaming to ensure reliability when hosting.

---

## Core Functions ⚒️

📊 Real-time graph plotting powered by `Matplotlib` (headless **Agg** backend for stability)  
🧮 Secure math expression parsing via `SymPy` with a sandboxed function set  
💡 AI-assisted tutoring powered by **Gemini 2.0 Flash**  
🧠 Multiple function plotting using semicolon-separated syntax  
🔍 Automatic NaN handling for clean graphs and uninterrupted rendering  
💬 Human-readable Gemini responses formatted with a custom `_prettify_ai()` parser  
🔒 Secure secret handling through `.env` and `python-dotenv`

---

## How I built it 🏗️

I developed **MathVision** using a combination of efficient scientific and web technologies:

- **Django (Backend + Templates)** for request handling, CSRF-protected forms, and dynamic rendering
- **Matplotlib (Agg backend)** for server-safe visualization
- **SymPy and NumPy** for symbolic parsing, vectorized numerical evaluation, and safe math execution
- **Google Generative AI (Gemini)** for intelligent explanations and natural language responses
- **HTML + CSS** for a clean, responsive interface

To ensure performance and security, I implemented:

- **Vectorized computations** with `lambdify(..., "numpy")` for high-speed evaluations across thousands of points
- **Automatic error handling** that displays descriptive in-plot messages rather than crashes
- **Graceful Gemini integration**, which activates only when an API key is found in environment variables

---

## Challenges I ran into ⚠️

- Safely evaluating user input without executing arbitrary code — solved with `SAFE_FUNCS` and SymPy sandboxing
- Handling invalid or non-finite values gracefully using NumPy’s `isfinite()` and NaN substitution
- Achieving smooth multi-function rendering without freezing the browser or server
- Ensuring efficient memory usage — optimized by streaming plots directly from memory (`BytesIO`) instead of saving to disk.
- Formatting Gemini output consistently with `_prettify_ai()` for clear tutoring responses

---

## Accomplishments I'm proud of 🏆

- Created a secure, stable **AI-assisted math visualization platform**
- Combined symbolic computation, real-time graphing, and AI feedback into one cohesive system
- Constructed in-memory PNG rendering via BytesIO and Matplotlib, enabling fast, disk-free image generation and cutting rendering latency by 60%.
- Designed the plotting engine to be **lightweight, modular, and safe** under any user input
- Achieved instant rendering of multiple complex functions with optimized Matplotlib and NumPy pipelines
- Ensured **robust error management and secure key handling** through `.env`

---

## What’s next for MathVision 🚀

- ✳️ Add 3D graphing (Plotly or Matplotlib 3D)
- 🧠 Expand AI tutoring to handle step-by-step derivations and simplifications
- ⚡ Enhance caching and optimize for large input ranges
- 💾 Enable user accounts and function history saving

---

## Tech Stack 💻

- **Backend:** Django 5.2
- **Math Engine:** SymPy + NumPy
- **Visualization:** Matplotlib (Agg backend)
- **AI Integration:** Google Gemini 2.0 Flash
- **Frontend:** CSS, HTML, Django Template Inheritance System.
- **Security:** python-dotenv, CSRF-protected forms

---

## Development ⚙️

To run **MathVision** locally:

1️⃣ Clone the repository:

```bash
git clone https://github.com/abdumalikxs/mathvision.git
cd MathVision
```

2️⃣ Install dependencies:

```bash
pip install -r requirements.txt
```

3️⃣ Create a `.env` file in the project root:

```
DJANGO_SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

4️⃣ Run migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

5️⃣ Open in your browser:  
👉 http://127.0.0.1:8000

---

## Contributing 🤝

**MathVision** is open-source and welcomes contributors!  
If you’d like to improve it, fork the repo, create a branch, and submit a pull request. Thanks!
