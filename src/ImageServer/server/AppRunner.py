import requests
import logging
import json
from .httpServer import HTTPServer
from functools import cached_property


class Config:
    def __init__(
        self,
        wcr_server_host: str,
        wcr_server_port: int,
        wcr_server_protocol: str,
        base_wz_code_path: str,
    ) -> None:
        self.wcr_server_host = wcr_server_host
        self.wcr_server_port = wcr_server_port
        self.wcr_server_protocol = wcr_server_protocol
        self.base_wz_code_path = base_wz_code_path

    def to_json(self) -> dict:
        return {
            "wcr_server_host": self.wcr_server_host,
            "base_wz_code_path": self.base_wz_code_path,
        }


class AppRunner:
    def __init__(
        self,
        wcr_server_host: str,
        wcr_server_port: int,
        wcr_server_protocol: str,
        base_wz_code_path: str,
    ) -> None:
        self.config = Config(
            wcr_server_host=wcr_server_host,
            wcr_server_port=wcr_server_port,
            wcr_server_protocol=wcr_server_protocol,
            base_wz_code_path=base_wz_code_path,
        )
        self.HTTPServer = HTTPServer(
            logger=self.logger
        )

    @cached_property
    def logger(self):
        logger = logging.getLogger(__name__)

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
        )

        file_handler = logging.FileHandler("logs/app_runner_log.log")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        
        return logger

    def run(self) -> None:
        self.logger.info(f"now config: {json.dumps(self.config.to_json())}")

        self.logger.info("start loading base_wz")
        self._load_base_wz()
        self.logger.info("complete loading base_wz")

        self.logger.info("start HTTPServer")
        self.HTTPServer.run()

    def _load_base_wz(self) -> None:
        if self.config.base_wz_code_path:
            base_wz_code_path = self.config.base_wz_code_path
            with open(base_wz_code_path) as f:
                self.base_wz = json.load(f)
        else:
            wcr_server_protocol = self.config.wcr_server_protocol
            wcr_server_host = self.config.wcr_server_host
            wcr_server_port = self.config.wcr_server_port

            url = f"{wcr_server_protocol}://{wcr_server_host}:{wcr_server_port}/code"
            response = requests.get(url)
            self.base_wz = json.load(response)