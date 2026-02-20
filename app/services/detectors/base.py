from dataclasses import dataclass


@dataclass
class DetectionResult:
    anomaly_score: float
    is_anomaly: bool
    risk_level: str
    model_type: str
    model_version: str


class BaseDetector:
    model_type = "base"
    model_version = "v0"

    def detect(self, event):
        raise NotImplementedError
