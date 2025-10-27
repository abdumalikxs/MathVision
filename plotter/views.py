from sympy import sympify, symbols, lambdify, sin, cos, tan, exp, log, sqrt, Abs
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as pyplot
from io import BytesIO
import os
import numpy
import matplotlib
matplotlib.use("Agg")


GEMINI_ENABLED = False
GEMINI_MODEL = None

try:
    import google.generativeai as genai
    key = getattr(settings, "GEMINI_API_KEY",
                  "") or os.environ.get("GEMINI_API_KEY")
    if key:
        genai.configure(api_key=key)
        GEMINI_MODEL = genai.GenerativeModel("gemini-2.0-flash")
        GEMINI_ENABLED = True
except Exception:
    pass


x = symbols("x")
SAFE_FUNCS = {
    "x": x,
    "sin": sin, "cos": cos, "tan": tan,
    "exp": exp, "log": log, "sqrt": sqrt, "abs": Abs
}


def _prettify_ai(text: str) -> str:
    """Formats Gemini output into neat readable text with minimal styling."""
    if not isinstance(text, str):
        return ""
    import re
    # Remove markdown bold and headers
    s = re.sub(r"[*_#`]+", "", text)
    # Normalize newlines
    s = s.replace("\r", "\n").strip()
    # Replace multiple newlines with one
    s = re.sub(r"\n{3,}", "\n\n", s)
    # Add consistent indentation for bullets
    s = re.sub(r"^\s*[\*-]\s+", "• ", s, flags=re.MULTILINE)
    # Capitalize first letter if missing
    if s and not s[0].isupper():
        s = s[0].upper() + s[1:]
    return s


def _clean_expr(expr: str) -> str:
    return expr.replace("^", "**")   # allowing '^' for power.


def _render_plot(f_str: str, xmin: float, xmax: float) -> bytes:
    fig, ax = pyplot.subplots(figsize=(6, 4), dpi=150)
    try:
        if xmin >= xmax:
            raise ValueError("xmin must be < xmax")

        exprs = [s.strip() for s in f_str.split(";") if s.strip()]
        if not exprs:
            exprs = ["sin(x)"]

        # list of 800 x-values between xmax and xmin
        X = numpy.linspace(xmin, xmax, 800)
        for expr in exprs:
            expr = _clean_expr(expr)
            sym = sympify(expr, locals=SAFE_FUNCS)  # right format
            # mathematical func  (vectorized indexing so it processes multiple values)
            f = lambdify(x, sym, "numpy")
            Y = f(X)
            # Handle NaN/Inf correctly
            Y = numpy.array(Y, dtype=float)
            # assigning NaN to all the invalid Y values. #Matplotlib skips NaN values so graph doestn break
            # negating the (False --> invalid values)
            Y[~numpy.isfinite(Y)] = numpy.nan
            ax.plot(X, Y, label=expr)

        ax.axhline(0, color="black", linewidth=0.3)  # y=0
        ax.axvline(0, color="black", linewidth=0.3)  # x=0
        ax.set_xlim(xmin, xmax)    # limit the size
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)  # func naming on right corner
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # informative title
        title_exprs = "; ".join(exprs)
        title_str = f"{title_exprs}   |   x in [{xmin}, {xmax}]"
        # optimized the length. If too long, truncate to keep the plot tidy
        if len(title_str) > 45:
            title_str = title_exprs[:25] + "..." + \
                f" |   x in [{xmin}, {xmax}]"
        ax.set_title(title_str)

    except Exception as e:
        ax.text(0.5, 0.5, f"Error: {e}", ha="center",
                va="center", transform=ax.transAxes)
        ax.axis("off")

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    pyplot.close(fig)
    return buf.getvalue()


@csrf_protect
def plot_page(request):
    f = request.GET.get("f", "sin(x)")
    xmin = request.GET.get("xmin", "-10")
    xmax = request.GET.get("xmax", "10")  # if missing set xmax to 10
    ai_answer = None
    ai_error = None

    # If user posted a question for Gemini
    if request.method == "POST":
        user_q = request.POST.get("question", "").strip()
        f = request.POST.get("f_hidden", f).strip() or f
        xmin = request.POST.get("xmin_hidden", xmin)
        xmax = request.POST.get("xmax_hidden", xmax)
        if user_q:
            if GEMINI_ENABLED and GEMINI_MODEL:
                try:
                    prompt = (
                        "You are a math tutor. Given a real-valued function f(x) and a range, "
                        "answer the user's question briefly and clearly.\n\n"
                        f"Function(s): {f}\n"
                        f"Range: x in [{xmin}, {xmax}]\n"
                        f"Question: {user_q}\n"
                        "If helpful, mention intercepts, monotonicity, curvature, extrema, "
                        "and asymptotic behavior within the range."
                    )
                    resp = GEMINI_MODEL.generate_content(prompt)
                    raw_text = getattr(
                        resp, "text", None) or "No response text."
                    ai_answer = _prettify_ai(raw_text)
                except Exception as e:
                    ai_error = f"Gemini error: {e}"
            else:
                ai_error = "Gemini is not configured. Put GEMINI_API_KEY in settings.py or env."

    ctx = {
        "f": f,
        "xmin": xmin,
        "xmax": xmax,
        "ai_answer": ai_answer,
        "ai_error": ai_error,
        "gemini_on": GEMINI_ENABLED,
    }
    return render(request, "plot_page.html", ctx)


def plot_image(request):
    # query string: f -> looks if no value, takes sin(x)
    f_str = request.GET.get("f", "sin(x)")
    xmin = float(request.GET.get("xmin", "-10"))
    xmax = float(request.GET.get("xmax", "10"))
    png = _render_plot(f_str, xmin, xmax)
    return HttpResponse(png, content_type="image/png")
