import os

from dataclasses import dataclass
from argparse import ArgumentParser, Namespace

from ...version import __version__
from ..auto_numbered import AutoNumberedEnum

__all__ = ["gp_parser", "App"]


def gp_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Chat Bot and Web Scraper")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="command to run")
    subparsers.add_parser("run", help="run app")
    subparsers.add_parser("do", help="do something")

    run_parser = subparsers.add_parser("run", help="run app")
    run_parser.add_argument("-d", "--debug", action="store_true", help="debug mode")
    run_parser.add_argument(
        "-r", "--release", action="store_true", help="release mode", default=True
    )

    do_parser = subparsers.add_parser("do", help="do something")
    do_subparsers = do_parser.add_subparsers(dest="action", help="action to do")
    scrap_parser = do_subparsers.add_parser("scrap", help="scrap data")
    scrap_parser.add_argument(
        "-o", "--output", help="output filename", default=None, required=False
    )
    do_subparsers.add_parser("pre", help="pretrain model")

    return parser


class Action(AutoNumberedEnum):
    run = ()
    scrap = ()
    pre = ()


@dataclass
class Args:
    action: Action = Action.run
    debug: bool = False
    scrap_path: str = os.path.join("assets", "data.json")


class App:
    def __init__(self) -> None:
        self.__args = Args()

    def check_args(self, nsp: Namespace) -> "App":
        if nsp.command == "run":
            if nsp.debug:
                if nsp.release:
                    raise RuntimeError("debug and release are mutually exclusive")
                self.__args.debug = True

        elif nsp.command == "do":
            if nsp.action == "scrap":
                self.__args.action = Action.scrap
                if nsp.output:
                    self.__args.scrap_path = nsp.output
            elif nsp.action == "pre":
                self.__args.action = Action.pre
            else:
                raise RuntimeError("invalid action")

        return self

    def run(self):
        if self.__args.action == Action.run:
            import logging
            import flet as ft
            from ...app.home import home_page
            from ..logger import init_logger

            init_logger(logging.DEBUG if self.__args.debug else logging.INFO)
            ft.app(target=home_page)

        elif self.__args.action == Action.scrap:
            from ...webSrap import run_spider

            run_spider(self.__args.scrap_path)

        elif self.__args.action == Action.pre:
            raise NotImplementedError("pretrain model")
