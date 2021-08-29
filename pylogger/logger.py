import logging
from typing import Optional

from pylogger.levels import Level


class Logger:
    __logger: logging.Logger
    __level: Level
    __module: Optional[str]

    @property
    def __formatter(self, module: Optional[str] = None) -> logging.Formatter:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.__module = module
        return formatter

    @property
    def module(self) -> str:
        name = self.__module
        if name is None:
            return ""
        return "[" + name.upper() + "]" + " - "

    def __init__(self, name: str, level: Level = Level.NOTSET):
        self.__level = level
        self.__logger = logging.getLogger(name=name)
        self.__logger.setLevel(level=level.value)

    def add_console_handler(self, level: Level = None):
        handler = logging.StreamHandler()
        handler.setLevel(level or self.__level)
        handler.setFormatter(self.__formatter)
        self.__logger.addHandler(hdlr=handler)

    def add_file_handler(self, filename: str, level: Level = None):
        handler = logging.FileHandler(filename=filename)
        handler.setLevel(level or self.__level)
        handler.setFormatter(self.__formatter)
        self.__logger.addHandler(hdlr=handler)

    def modulelogger(func):
        def wrap(*args, **kwargs):
            self = args[0]
            msg = self.module + kwargs.get("msg", args[1])
            args = (self, msg, *args[1 if "msg" in kwargs.keys() else 2:])
            return func(*args, **kwargs)
        return wrap

    def set_module(self, modulename: str) -> 'Logger':
        self.__module = modulename
        
    def add_module(self, modulename: str) -> 'Logger':
        logger = self
        logger.set_module(modulename)
        return logger

    @modulelogger
    def log(self, msg: str, level: Level = Level.NOTSET, show_stack: bool = False):
        self.__logger.log(msg=msg, level=level.value, stack_info=show_stack, stacklevel=2)

    @modulelogger
    def debug(self, msg: str, show_stack: bool = False):
        self.__logger.debug(msg=msg, stack_info=show_stack, stacklevel=2)

    @modulelogger
    def info(self, msg: str, show_stack: bool = False):
        self.__logger.info(msg=msg, stack_info=show_stack, stacklevel=2)

    @modulelogger
    def error(self, msg: str, show_stack: bool = False):
        self.__logger.error(msg=msg, stack_info=show_stack, stacklevel=2)

    @modulelogger
    def critical(self, msg: str, show_stack: bool = False):
        self.__logger.critical(msg=msg, stack_info=show_stack, stacklevel=2)
