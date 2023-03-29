from flask import Blueprint, request, render_template, session

create_payloads_bp = Blueprint("create_payloads", __name__)


@create_payloads_bp.route("/payloads", methods=("GET", "POST"))
def create_payloads():
    if request.method == "POST":
        # Retrieve form data
        username = session.username
        session_id = session.session_id
        # Render template with form data
        return render_template(
            "payloads.html", username=username, session_id=session_id
        )

    # Render form template
    return render_template("payloads.html")
