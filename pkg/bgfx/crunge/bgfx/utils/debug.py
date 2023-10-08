#! /usr/bin/python

import logging
import ctypes

# output "logging" messages to DbgView via OutputDebugString (Windows only!)
OutputDebugString = ctypes.windll.kernel32.OutputDebugStringW


class DbgViewHandler(logging.Handler):
    def emit(self, record):
        OutputDebugString(self.format(record))


log = logging.getLogger("output.debug.string.example")


def config_logging():

    # format
    fmt = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d [%(thread)5s] %(levelname)-8s %(funcName)-20s %(lineno)d %(message)s",
        datefmt="%Y:%m:%d %H:%M:%S",
    )

    log.setLevel(logging.DEBUG)

    # "OutputDebugString\DebugView"
    ods = DbgViewHandler()
    ods.setLevel(logging.DEBUG)
    ods.setFormatter(fmt)
    log.addHandler(ods)

    # "Console"
    con = logging.StreamHandler()
    con.setLevel(logging.DEBUG)
    con.setFormatter(fmt)
    log.addHandler(con)


def main():

    log.debug("debug message")
    log.info("info message")
    log.warn("warn message")
    log.error("error message")
    log.critical("critical message")


if __name__ == "__main__":

    config_logging()

    main()
