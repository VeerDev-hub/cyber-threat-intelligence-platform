from flask import Blueprint, jsonify
from flask_login import login_required
from app.analytics.services import (
    summary_metrics,
    top_attacker_ips,
    top_target_ports,
    attack_types_distribution,
    risk_levels_distribution,
)

analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


@analytics_bp.route("/summary", methods=["GET"])
@login_required
def analytics_summary():
    return jsonify(summary_metrics()), 200


@analytics_bp.route("/top-ips", methods=["GET"])
@login_required
def analytics_top_ips():
    return jsonify(top_attacker_ips()), 200


@analytics_bp.route("/top-ports", methods=["GET"])
@login_required
def analytics_top_ports():
    return jsonify(top_target_ports()), 200


@analytics_bp.route("/attack-types", methods=["GET"])
@login_required
def analytics_attack_types():
    return jsonify(attack_types_distribution()), 200


@analytics_bp.route("/risk-levels", methods=["GET"])
@login_required
def analytics_risk_levels():
    return jsonify(risk_levels_distribution()), 200
