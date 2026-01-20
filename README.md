# 🛡️ Sentinel: AI-Powered Log Anomaly Detector

### 🚀 Overview
**Sentinel** is an intelligent monitoring agent designed to enhance DevOps observability using **Unsupervised Machine Learning**.

Traditional monitoring tools (like Datadog or Splunk) often rely on static, rule-based alerts (e.g., `if "ERROR" in log`). However, these tools fail to catch **"Unknown Unknowns"**—subtle deviations in system behavior that don't match pre-defined rules.

Sentinel solves this by using the **Isolation Forest** algorithm to learn the **baseline pattern** of normal operations. It then flags *any* deviation from this baseline as an anomaly, allowing SRE teams to detect latent issues such as memory leaks, security breaches, or performance degradation before they cause an outage.

### 🧠 The Intelligence
* **Algorithm:** Isolation Forest (Scikit-Learn).
* **Technique:** Outlier Detection in High-Dimensional Vector Space.
* **Why Isolation Forest?** It is particularly efficient at identifying anomalies in high-volume datasets because it explicitly isolates anomalies rather than profiling normal data points, making it faster and less computationally expensive.

### 🛠️ Tech Stack
* **Language:** Python 3.9
* **Machine Learning:** Scikit-Learn (Isolation Forest)
* **Data Processing:** Pandas, NumPy
* **Vectorization:** TF-IDF (Term Frequency-Inverse Document Frequency)

### 📊 How it Works
1. **Training Phase:** The model ingests a dataset of "Normal" logs to understand the standard operational vector space.
2. **Monitoring Phase:** It scans live log streams in real-time.
3. **Detection:** If a log entry's vector distance significantly deviates from the learned cluster, it is flagged as an `🔴 ANOMALY`.

### 🔮 Future Scope
* **Cloud Integration:** Integration with **AWS CloudWatch Logs** via Kinesis Firehose for real-time streaming analysis.
* **Automated Remediation:** Triggering **AWS Lambda** functions to restart services or block IPs upon high-confidence anomaly detection.
* **Feedback Loop:** Implementing a "Human-in-the-Loop" mechanism to retrain the model based on SRE feedback for false positives.

---
*Developed as a Strategic Initiative to demonstrate Proactive AIOps capabilities.*
