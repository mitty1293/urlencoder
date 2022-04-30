import os
from logging import basicConfig

from flask import Flask, redirect, render_template, request, url_for

# Configure logging
# If FLASK_ENV=production, then level=WARNING
# If FLASK_ENV=development, then level=DEBUG
basicConfig(
    filename="/app/urlencoder/logs/app.log",
    format="%(asctime)s\t%(levelname)s\t%(filename)s\t%(module)s\tline:%(lineno)d\t%(message)s",
)

# Create an instance of the Flask application
app = Flask(__name__, instance_path="/run/secrets", instance_relative_config=True)

# Load the conig
config_type = {
    "development": "urlencoder.config.DevelopmentConfig",
    "production": "urlencoder.config.ProductionConfig",
}
app.config.from_object(config_type.get(os.getenv("FLASK_ENV", "production")))

# Routing
@app.route("/", methods=["GET", "POST"])
def index():
    # GET
    if request.method == "GET":
        return render_template("index.html")

    # POST
    req_dict = request.form.to_dict()
    if "encode_btn" in req_dict.keys():
        # Encode
        outputtext = f"Encode {req_dict.get('inputtext')}"
        app.logger.debug(outputtext)
    elif "decode_btn" in req_dict.keys():
        # Decode
        outputtext = f"Decode {req_dict.get('inputtext')}"
        app.logger.debug(outputtext)
    return render_template("index.html", outputtext=outputtext)
