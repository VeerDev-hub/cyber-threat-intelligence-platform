from app.analytics.services import (
    summary_metrics,
    top_attacker_ips,
    top_target_ports,
    attack_types_distribution,
)


def get_summary_metrics():
    return summary_metrics()


def get_top_attacker_ips(limit=5):
    return top_attacker_ips(limit=limit)


def get_top_target_ports(limit=5):
    return top_target_ports(limit=limit)


def get_attack_types_distribution():
    return attack_types_distribution()
