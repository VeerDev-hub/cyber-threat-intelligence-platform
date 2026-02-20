from app.services.detectors.base import BaseDetector, DetectionResult


class MLDetector(BaseDetector):
    model_type = "ml_stub"
    model_version = "v1"

    def detect(self, event):
        severity = int(event.get("severity", 0) or 0)
        destination_port = event.get("destination_port")
        attack_type = str(event.get("attack_type", "unknown"))

        base = min(max(severity / 10.0, 0.0), 1.0)
        port_factor = 0.1 if destination_port in {22, 3389, 445} else 0.0
        attack_factor = 0.1 if attack_type in {"brute_force", "port_scan"} else 0.0

        anomaly_score = min(1.0, round(base + port_factor + attack_factor, 4))
        is_anomaly = anomaly_score >= 0.7

        if anomaly_score >= 0.8:
            risk_level = "high"
        elif anomaly_score >= 0.5:
            risk_level = "medium"
        else:
            risk_level = "low"

        return DetectionResult(
            anomaly_score=anomaly_score,
            is_anomaly=is_anomaly,
            risk_level=risk_level,
            model_type=self.model_type,
            model_version=self.model_version,
        )
