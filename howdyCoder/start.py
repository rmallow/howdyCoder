from .mainframe import mainframe

import logging

import argparse
import threading
import traceback


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--ui", help="Start the ui", action="store_true")
    parser.add_argument("-s", "--server", help="Start the server", action="store_true")
    parser.add_argument(
        "-l",
        "--local",
        help="Start both ui and server for full local app",
        action="store_true",
    )
    args, _ = parser.parse_known_args()

    isLocal: bool = False
    if args.local:
        isLocal = True
    # init server
    if args.server or args.local:
        main = mainframe(isLocal)
        mainframeThread = threading.Thread(target=main.init)
        mainframeThread.start()

    # If ui arg passed in then start, otherwise do not import
    if args.ui or args.local:
        try:
            from .ui import howdyCoder
        except ModuleNotFoundError as e:
            logging.critical(
                "UI arg passed (-u) or local arg (-l) but ui modules not installed"
            )
            logging.critical(f"Module not found: {e.name} at path: {e.path}")
            traceback.print_exception(e)
        else:
            # if ui is present we will allow the ui to run it
            howdyCoder.start(isLocal)
    elif args.server:
        main.cmdStart(None)
