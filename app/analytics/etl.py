from app.services.processing_service import process_pending_raw_logs


def process_raw_logs(limit=100, detector=None):
    return process_pending_raw_logs(limit=limit, detector=detector)
