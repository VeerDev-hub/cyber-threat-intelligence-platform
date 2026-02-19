from flask import Blueprint, render_template
from flask_login import login_required
from app.analytics.services import (
    summary_metrics,
    attack_types_distribution,
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@login_required
def dashboard_home():
    summary = summary_metrics() or {}
    attack_types = attack_types_distribution() or []

    summary.setdefault("total_attacks", 0)
    summary.setdefault("average_severity", 0)
    summary.setdefault("severity_distribution", [])

    return render_template(
        "dashboard/overview.html",
        summary=summary,
        attack_types=attack_types,
    )
