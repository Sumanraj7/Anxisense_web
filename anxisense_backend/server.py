from waitress import serve
from app import app
import os

if __name__ == "__main__":
    print("Starting AnxiSense Production Server on 0.0.0.0:5000...")
    # Use 4 threads for concurrent request handling
    serve(app, host='0.0.0.0', port=5000, threads=6)
