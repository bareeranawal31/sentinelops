from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from SentinelOps sample app!"

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/simulate-load")
def simulate_load():
    total = sum(random.random() for _ in range(10**6))
    return {"status": "load simulated", "result": total}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
