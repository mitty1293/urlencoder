import os
from logging import DEBUG, basicConfig

from flask import Flask, render_template

# Configure logging
basicConfig(
    filename="/app/urlencoder/logs/app.log",
    level=DEBUG,
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
