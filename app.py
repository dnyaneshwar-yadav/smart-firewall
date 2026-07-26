from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)


from firewall.database import Database
from firewall.rules import RuleManager
from firewall.logger import Logger
from firewall.iptables_manager import IPTablesManager

app = Flask(__name__)

# =====================================================
# Dashboard
# =====================================================

@app.route("/")
def dashboard():

    db = Database()

    total_packets = db.get_total_packets()
    allowed_packets = db.get_allowed_packets()
    blocked_packets = db.get_blocked_packets()
    total_rules = db.get_total_rules()
    recent_logs = db.get_recent_logs()

    db.close()

    return render_template(
        "dashboard.html",
        total_packets=total_packets,
        allowed_packets=allowed_packets,
        blocked_packets=blocked_packets,
        total_rules=total_rules,
        recent_logs=recent_logs
    )


# =====================================
# Dashboard API
# =====================================

@app.route("/dashboard-data")
def dashboard_data():

    db = Database()

    data = {

        "total_packets": db.get_total_packets(),
        "allowed_packets": db.get_allowed_packets(),
        "blocked_packets": db.get_blocked_packets(),
        "total_rules": db.get_total_rules(),
        "recent_logs": db.get_recent_logs()

    }

    db.close()

    return data

# =====================================================
# Rules
# =====================================================

@app.route("/rules", methods=["GET", "POST"])
def rules():

    manager = RuleManager()

    if request.method == "POST":

        rule_type = request.form["rule_type"]
        value = request.form["value"]

        manager.add_rule(rule_type, value)

        manager.close()

        return redirect("/rules")

    all_rules = manager.get_rules()

    manager.close()

    return render_template(
        "rules.html",
        rules=all_rules
    )


# =====================================================
# Delete Rule
# =====================================================

@app.route("/delete-rule/<int:rule_id>")
def delete_rule(rule_id):

    manager = RuleManager()

    manager.delete_rule(rule_id)

    manager.close()

    return redirect("/rules")


# =====================================================
# Apply Rules
# =====================================================

@app.route("/apply-rules")
def apply_rules():

    manager = RuleManager()

    manager.apply_rules()

    manager.close()

    return redirect("/rules")


# =====================================================
# Firewall
# =====================================================

@app.route("/firewall")
def firewall():

    manager = IPTablesManager()

    rules = manager.list_rules()

    return render_template(
        "firewall.html",
        rules=rules
    )


# =====================================================
# Flush Firewall
# =====================================================

@app.route("/flush-firewall")
def flush_firewall():

    manager = IPTablesManager()

    manager.flush()

    return redirect("/firewall")


# =====================================================
# Logs
# =====================================================

@app.route("/logs")
def logs():

    logger = Logger()

    keyword = request.args.get("search")
    action = request.args.get("action")

    if keyword:

        logs = logger.search_logs(keyword)

    elif action and action != "ALL":

        logs = logger.filter_logs(action)

    else:

        logs = logger.get_logs()

    logger.close()

    return render_template(
        "logs.html",
        logs=logs
    )


# =====================================
# Logs API
# =====================================

@app.route("/logs-data")
def logs_data():

    logger = Logger()

    logs = logger.get_logs()

    logger.close()

    return {

        "logs": logs

    }

# =====================================================
# Export Logs
# =====================================================

@app.route("/export-logs")
def export_logs():

    logger = Logger()

    filepath = logger.export_logs()

    logger.close()

    return send_file(
        filepath,
        as_attachment=True
    )


# =====================================================
# Clear Logs
# =====================================================

@app.route("/clear-logs")
def clear_logs():

    logger = Logger()

    logger.clear_logs()

    logger.close()

    return redirect("/logs")


# =====================================================
# Analytics
# =====================================================

@app.route("/analytics")
def analytics():

    db = Database()

    total_packets = db.get_total_packets()
    allowed_packets = db.get_allowed_packets()
    blocked_packets = db.get_blocked_packets()
    total_rules = db.get_total_rules()

    protocol_data = db.get_protocol_counts()
    action_data = db.get_allow_block_stats()

    db.close()

    return render_template(
        "analytics.html",
        total_packets=total_packets,
        allowed_packets=allowed_packets,
        blocked_packets=blocked_packets,
        total_rules=total_rules,
        protocol_data=protocol_data,
        action_data=action_data
    )


# =====================================
# Analytics API
# =====================================

@app.route("/analytics-data")
def analytics_data():

    db = Database()

    data = {

        "total_packets": db.get_total_packets(),
        "allowed_packets": db.get_allowed_packets(),
        "blocked_packets": db.get_blocked_packets(),
        "total_rules": db.get_total_rules(),
        "protocol_data": db.get_protocol_counts(),
        "action_data": db.get_allow_block_stats()

    }

    db.close()

    return data

# =====================================================
# Settings
# =====================================================

@app.route("/settings")
def settings():

    return render_template("settings.html")



# =====================================================
# Run Application
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
