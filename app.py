from flask import Flask, render_template, request
import math
import random

app = Flask(__name__)

def predict_traffic(history, periods=6):
    """Simple linear-trend prediction using least-squares regression."""
    n = len(history)
    if n == 0:
        return []
    if n == 1:
        return [round(max(0, history[0]), 2) for _ in range(periods)]

    xs = list(range(n))
    x_mean = sum(xs) / n
    y_mean = sum(history) / n
    denom = sum((x - x_mean) ** 2 for x in xs)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, history)) / denom if denom else 0
    intercept = y_mean - slope * x_mean
    predictions = []
    for step in range(n, n + periods):
        value = max(0, intercept + slope * step)
        predictions.append(round(value, 2))
    return predictions

def classify_load(value, capacity):
    ratio = value / capacity if capacity > 0 else 0
    if ratio >= 0.85:
        return "High", "high"
    if ratio >= 0.60:
        return "Moderate", "moderate"
    return "Normal", "normal"

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    history_text = "35, 42, 38, 50, 57, 54, 63, 68"
    capacity_text = "100"
    labels = [f"T{i+1}" for i in range(8)]
    history = [35, 42, 38, 50, 57, 54, 63, 68]
    predictions = predict_traffic(history)
    capacity = 100

    if request.method == "POST":
        history_text = request.form.get("history", "").strip()
        capacity_text = request.form.get("capacity", "100").strip()
        try:
            history = [float(v.strip()) for v in history_text.split(",") if v.strip()]
            if len(history) < 2:
                raise ValueError("Please enter at least two traffic values.")
            if len(history) > 30:
                raise ValueError("Please enter no more than 30 traffic values.")
            if any(v < 0 for v in history):
                raise ValueError("Traffic values cannot be negative.")
            capacity = float(capacity_text)
            if capacity <= 0:
                raise ValueError("Network capacity must be greater than zero.")
            if not all(math.isfinite(v) for v in history) or not math.isfinite(capacity):
                raise ValueError("Please enter valid numeric values.")
            predictions = predict_traffic(history)
            labels = [f"T{i+1}" for i in range(len(history))]
        except (ValueError, OverflowError) as exc:
            error = str(exc) or "Please check the values and try again."
            history = []
            predictions = []
            labels = []
            capacity = 100

    current = history[-1] if history else 0
    next_value = predictions[0] if predictions else 0
    status, status_class = classify_load(next_value, capacity)
    chart_data = {
        "historyLabels": labels,
        "historyValues": history,
        "predictionLabels": [f"Future {i+1}" for i in range(len(predictions))],
        "predictionValues": predictions,
    }
    return render_template(
        "index.html",
        error=error,
        history_text=history_text,
        capacity_text=capacity_text,
        history=history,
        predictions=predictions,
        current=current,
        next_value=next_value,
        status=status,
        status_class=status_class,
        chart_data=chart_data,
    )

if __name__ == "__main__":
    app.run(debug=True)
