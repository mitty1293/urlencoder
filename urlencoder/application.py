import os
from logging import basicConfig

from flask import Flask, render_template

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


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
