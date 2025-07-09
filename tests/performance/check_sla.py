import csv
import sys

history = "locust_stats_history.csv"
rows = list(csv.DictReader(open(history)))
last = rows[-1]
try:
    p95 = float(last.get("95%", 0))
    total = float(last.get("Total Request Count", 0))
    failures = float(last.get("Total Failure Count", 0))
except ValueError:
    sys.exit("invalid stats")
fail_rate = failures / total if total else 0
print(f"p95 latency: {p95} ms, fail rate: {fail_rate*100:.2f}%")
if p95 > 250 or fail_rate > 0.01:
    sys.exit("SLA breach")
