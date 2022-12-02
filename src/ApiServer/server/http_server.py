import logging

from aiohttp import web

from .config import Config
from .http_handler import HttpHandler


class HttpServer:
    def __init__(
        self,
        logger: logging.Logger,
        config: Config,
    ) -> None:
        self.logger = logger
        self.app = web.Application()
        self.config = config
        self.HttpHandler = HttpHandler(
            logger=self.logger,
            config=config,
        )
        self.routes = self.HttpHandler.get_routes()
        self.app.add_routes(self.routes)

    def run(
        self,
    ) -> None:
        self.logger.info(f"server start! routing info: {self.routes}")
        web.run_app(self.app, port=7000)
