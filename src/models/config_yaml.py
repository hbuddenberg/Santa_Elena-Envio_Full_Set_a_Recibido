import pprint
from typing import List

import yaml
from pydantic import BaseModel

from .replace_placeholders import replace_placeholders


class LocalPathConfig(BaseModel):
    main: str
    source: str
    config: str
    modules: str
    models: str
    templates: str
    logs: str


class DrivePathConfig(BaseModel):
    # main: str
    root_path: str
    in_progress: str
    done: str


class PathConfig(BaseModel):
    local: LocalPathConfig
    drive: DrivePathConfig


class SMTPConfig(BaseModel):
    user: str
    password: str
    server: str
    port: int


class APIConfig(BaseModel):
    scopes: List[str]
    credentials: str
    token: str


class MailTemplateConfig(BaseModel):
    report: str
    receiver: str
    empty: str


class MailSenderReportConfig(BaseModel):
    to: str
    cc: str
    cco: str


class MailSenderConfig(BaseModel):
    report: MailSenderReportConfig


class MailConfigBase(BaseModel):
    smtp: SMTPConfig
    api: APIConfig


class MailConfig(BaseModel):
    config: MailConfigBase
    template: MailTemplateConfig
    sender: MailSenderConfig


class Configuration(BaseModel):
    path: PathConfig
    mail: MailConfig


def load_config(file_path: str):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    config_data = replace_placeholders(config_data)
    config_data = Configuration(**config_data)
    return config_data


def main(file_path: str):
    config = load_config(file_path)
    pprint.pp(config)


# Ejemplo de uso
if __name__ == "__main__":
    file_path = "/Volumes/Resources/Development/SmartBots/Santa_Elena-Envio_Full_Set_a_Recibido/src/configuration/configuracion.yaml"
    main(file_path)
