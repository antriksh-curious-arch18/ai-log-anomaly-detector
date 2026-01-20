import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class LogAnomalyDetector:
    """
    AI-Driven Anomaly Detection System for DevOps Logs.
    
    This class utilizes Unsupervised Machine Learning (Isolation Forest) to establish 
    a baseline of 'normal' system behavior and detect outliers (anomalies) in 
    log patterns without requiring labeled training data.
    """

    def __init__(self, contamination=0.05):
        """
        Initializes the Anomaly Detector.

        Args:
            contamination (float): The expected proportion of outliers in the dataset.
                                   0.05 implies we expect ~5% of live logs to be anomalies.
        """
        # TF-IDF converts text logs into numerical vectors
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Isolation Forest is effective for high-dimensional data anomaly detection
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_trained = False

    def train(self, logs):
        """
        Trains the model to understand the baseline patterns of normal operations.
        
        Args:
            logs (list): A list of strings representing historical normal logs.
        """
        print(f"🧠  Learning Log Patterns from {len(logs)} records (Training Phase)...")
        
        # specific vectorization of logs
        X = self.vectorizer.fit_transform(logs)
        
        # Train the Isolation Forest model
        self.model.fit(X)
        self.is_trained = True
        print("✅  Model Trained successfully. Operational baseline established.")

    def predict(self, new_logs):
        """
        Scans a new stream of logs to detect if they are Normal or Anomalies.
        
        Args:
            new_logs (list): A list of strings representing live logs to analyze.
            
        Returns:
            DataFrame: A pandas DataFrame containing the log message and its status.
        """
        if not self.is_trained:
            raise Exception("Model error: The model must be trained before prediction.")

        print(f"🔍  Scanning {len(new_logs)} live logs for anomalies...")
        
        # Transform new logs into the same vector space as the training data
        X_new = self.vectorizer.transform(new_logs)
        
        # Predict: -1 indicates an Anomaly, 1 indicates Normal
        predictions = self.model.predict(X_new)
        
        # Generate a structured report
        results = pd.DataFrame({
            'Log_Message': new_logs,
            'Status': ['🔴 ANOMALY' if p == -1 else '🟢 Normal' for p in predictions]
        })
        
        return results

# ==========================================
# SIMULATION DATASET
# ==========================================

# 1. Normal Traffic Patterns (50 entries)
# Represents standard operational logs seen during healthy system state.
NORMAL_TRAFFIC_BASE = [
    "200 OK: GET /api/v1/users/profile - Latency 120ms",
    "200 OK: GET /api/v1/products/list - Latency 110ms",
    "200 OK: POST /api/v1/auth/login - Success",
    "INFO: Database connection established pool_size=10",
    "INFO: Cache refreshed successfully via Redis",
    "200 OK: GET /home/index.html - Latency 90ms",
    "200 OK: GET /assets/logo.png - Latency 20ms",
    "INFO: Cron job 'daily_cleanup' completed successfully",
    "200 OK: POST /api/v1/cart/add - Success",
    "INFO: Metrics pushed to Prometheus gateway"
]
# Multiplying the base list to simulate a larger dataset of 50 logs
NORMAL_TRAFFIC = NORMAL_TRAFFIC_BASE * 5

# 2. Anomalous Traffic Patterns (50 entries)
# Represents security threats, system failures, and performance spikes.
ANOMALY_BASE = [
    "401 Unauthorized: Failed login attempt from IP 192.168.1.50",
    "500 Internal Server Error: Database deadlock detected in transaction",
    "FATAL: Application panicked due to NullPointer Exception",
    "403 Forbidden: SQL Injection attempt detected in query param OR 1=1",
    "WARN: CPU usage spiked to 99% for process 'miner'",
    "ERROR: Connection refused to upstream payment gateway",
    "CRITICAL: Disk usage on /var/log reached 98%",
    "ALERT: Suspicious outbound traffic detected to known botnet IP",
    "503 Service Unavailable: Kubernetes Pod evicted due to OOMKilled",
    "SECURITY: Multiple failed SSH login attempts for root user"
]
# Multiplying to simulate a burst of issues (50 logs)
ATTACK_TRAFFIC = ANOMALY_BASE * 5

# ==========================================
# MAIN EXECUTION BLOCK
# ==========================================
if __name__ == "__main__":
    print("🛡️  INITIALIZING LOG SENTINEL AI...\n")
    
    # Initialize the Agent
    sentinel = LogAnomalyDetector(contamination=0.1)
    
    # Step 1: Train on Normal Data
    # The model learns what "Good" looks like.
    sentinel.train(NORMAL_TRAFFIC)
    print("-" * 70)

    # Step 2: Live Monitoring Simulation
    # We mix normal traffic with attack traffic to test the detector.
    # Creating a mixed stream: 10 Normal -> 50 Attacks -> 10 Normal
    live_stream = NORMAL_TRAFFIC[:10] + ATTACK_TRAFFIC + NORMAL_TRAFFIC[-10:]
    
    results = sentinel.predict(live_stream)

    # Step 3: Reporting
    print("\n📊  LIVE MONITORING REPORT (Anomalies Only):")
    print("-" * 70)
    
    anomaly_count = 0
    for index, row in results.iterrows():
        if row['Status'] == '🔴 ANOMALY':
            anomaly_count += 1
            print(f"{row['Status']} DETECTED: {row['Log_Message']}")
            
    print("-" * 70)
    print(f"✅  Scan Complete. Total Anomalies Detected: {anomaly_count}")
    print(f"    (Note: Normal logs are suppressed to reduce noise)")