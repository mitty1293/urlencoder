import os
import urllib.parse
from logging import basicConfig

from flask import Flask, render_template, request

# Configure logging
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
    match request.form.to_dict():
        # Encode
        case {'inputtext': inputtext, 'encode_btn': encode_btn, 'outputtext': outputtext}:
            outputtext = urllib.parse.quote(inputtext, safe=":/")
        # Decode
        case {'inputtext': inputtext, 'decode_btn': decode_btn, 'outputtext': outputtext}:
            outputtext = urllib.parse.unquote(inputtext)
    return render_template("index.html", inputtext=inputtext, outputtext=outputtext)
