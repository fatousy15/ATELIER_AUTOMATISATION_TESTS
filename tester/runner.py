import datetime
from tester.tests import run_all

def run():
    results = run_all()
    
    latencies = [r["latency_ms"] for r in results if r["latency_ms"] > 0]
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    total = len(results)
    
    avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0
    sorted_latencies = sorted(latencies)
    p95_index = int(len(sorted_latencies) * 0.95) - 1
    p95_latency = sorted_latencies[max(p95_index, 0)] if sorted_latencies else 0
    error_rate = round(failed / total, 3) if total > 0 else 0

    return {
        "api": "Agify",
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "error_rate": error_rate,
            "latency_ms_avg": avg_latency,
            "latency_ms_p95": p95_latency
        },
        "tests": results
    }
