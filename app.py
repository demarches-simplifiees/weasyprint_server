import os
import sys
import logging
from flask import Flask, request, make_response
from weasyprint import HTML
import sentry_sdk
from custom_fetcher import custom_url_fetcher

LOG_PATH = os.path.join(os.path.abspath(os.getcwd()), "log")
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE = os.path.join(LOG_PATH, "weasyprint.log")

logger = logging.getLogger("weasyprint")
logger.addHandler(logging.FileHandler(LOG_FILE))


def before_send(event, _hint):
    # Redact the request data to avoid sending sensitive information
    if "request" in event and "data" in event["request"]:
        event["request"]["data"] = "REDACTED"
    return event


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    enable_tracing=True,
    traces_sample_rate=1.0,
    before_send=before_send,
)


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        try:
            app.config["BASE_URL"] = os.environ["BASE_URL"]
        except KeyError:
            print("missing BASE_URL env var to fetch the assets (css, images ...)")
            sys.exit(1)
    else:
        app.config.from_mapping(test_config)

    @app.route("/pdf", methods=["POST"])
    def pdf():
        request_data = request.get_json()
        string_html = request_data["html"]
        html = HTML(
            string=string_html,
            base_url=app.config["BASE_URL"],
            url_fetcher=custom_url_fetcher,
        )
        try:
            generated_pdf = html.write_pdf()
        # See the hack in custom_fetcher.py
        except AttributeError:
            sentry_sdk.capture_message("An asset is missing")
            return make_response({"error": "an asset is missing"}, 500)

        response = make_response(generated_pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline;filename=fichier"
        return response

    @app.route("/ping", methods=["GET"])
    def ping():
        if os.path.isfile("maintenance"):
            return make_response({}, 404)

        return make_response({}, 200)

    return app
