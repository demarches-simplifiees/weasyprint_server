import os
import sys
import logging
from flask import Flask, request, make_response
from weasyprint import HTML

LOG_PATH = os.path.join(os.path.abspath(os.getcwd()), "log")
LOG_FILE = os.path.join(LOG_PATH, "weasyprint.log")

logger = logging.getLogger("weasyprint")
logger.addHandler(logging.FileHandler(LOG_FILE))

try:
    BASE_URL = os.environ["BASE_URL"]
except KeyError:
    print("missing BASE_URL env var to fetch the assets (css, images ...)")
    sys.exit(1)

app = Flask(__name__)


@app.route("/pdf", methods=["POST"])
def pdf():
    request_data = request.get_json()
    string_html = request_data["html"]
    html = HTML(string=string_html, base_url=BASE_URL)
    pdf = html.write_pdf()
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;filename=fichier"
    return response
