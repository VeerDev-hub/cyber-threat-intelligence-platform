from flask import Blueprint
from flask_login import login_required

from app.core.responses import success_response
from app.services.analytics_service import (
    get_summary_metrics,
    get_top_attacker_ips,
    get_top_target_ports,
    get_attack_types_distribution,
)


analytics_v1_bp = Blueprint("analytics_v1", __name__, url_prefix="/analytics")


@analytics_v1_bp.route("/summary", methods=["GET"])
@login_required
def analytics_summary():
    return success_response(data=get_summary_metrics(), status_code=200)


@analytics_v1_bp.route("/top-ips", methods=["GET"])
@login_required
def analytics_top_ips():
    return success_response(data=get_top_attacker_ips(), status_code=200)


@analytics_v1_bp.route("/top-ports", methods=["GET"])
@login_required
def analytics_top_ports():
    return success_response(data=get_top_target_ports(), status_code=200)


@analytics_v1_bp.route("/attack-types", methods=["GET"])
@login_required
def analytics_attack_types():
    return success_response(data=get_attack_types_distribution(), status_code=200)
