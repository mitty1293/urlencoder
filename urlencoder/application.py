import logging
import os
from logging import DEBUG, basicConfig

from flask import Flask, render_template

basicConfig(
    filename="./logs/app.log",
    level=DEBUG,
    format="%(asctime)s\t%(levelname)s\t%(filename)s\t%(module)s\tline:%(lineno)d\t%(message)s",
)

config_type = {
    "development": "config.DevelopmentConfig",
    "production": "config.ProductionConfig",
}

app = Flask(__name__, instance_path="/run/secrets", instance_relative_config=True)
app.config.from_object(config_type.get(os.getenv("FLASK_CONFIG_TYPE", "production")))
