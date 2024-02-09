import os
import sys
import logging
from flask import Flask, request, make_response
from weasyprint import HTML
from custom_fetcher import custom_url_fetcher

LOG_PATH = os.path.join(os.path.abspath(os.getcwd()), "log")
LOG_FILE = os.path.join(LOG_PATH, "weasyprint.log")

logger = logging.getLogger("weasyprint")
logger.addHandler(logging.FileHandler(LOG_FILE))


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
            response = make_response({"error": "an asset is missing"}, 500)
            return response

        response = make_response(generated_pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline;filename=fichier"
        return response

    return app
