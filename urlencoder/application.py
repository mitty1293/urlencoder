import os
import urllib.parse
from logging import basicConfig

from flask import Flask, render_template, request

# Configure logging
# If FLASK_ENV=production, then level=WARNING
# If FLASK_ENV=development, then level=DEBUG
basicConfig(
    filename="/app/logs/urlencoder.log",
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
    inputtext = req_dict.get("inputtext")
    if "encode_btn" in req_dict.keys():
        # Encode
        outputtext = urllib.parse.quote(inputtext, safe=":/")
    elif "decode_btn" in req_dict.keys():
        # Decode
        outputtext = urllib.parse.unquote(inputtext)
    return render_template("index.html", inputtext=inputtext, outputtext=outputtext)
