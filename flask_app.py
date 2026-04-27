from flask import Flask, render_template, jsonify
from tester.runner import run
from storage import save_run, list_runs

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html", runs=list_runs())

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", runs=list_runs())

@app.route("/run")
def run_tests():
    result = run()
    save_run(result)
    return jsonify(result)

@app.route("/health")
def health():
    runs = list_runs(limit=1)
    if runs:
        last = runs[0]
        status = "OK" if last["summary"]["error_rate"] < 0.5 else "DEGRADED"
        return jsonify({
            "status": status,
            "last_run": last["timestamp"],
            "error_rate": last["summary"]["error_rate"]
        })
    return jsonify({"status": "NO_DATA"})

@app.route("/export")
def export():
    runs = list_runs(limit=100)
    return jsonify(runs)

if __name__ == "__main__":
    app.run(debug=True)
