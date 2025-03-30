import os
import argparse
import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger("DirectoryWatcher")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class DirectoryCreationHandler(FileSystemEventHandler):
    def __init__(self, destination, debug=False):
        self.destination = destination
        self.debug = debug

    def on_created(self, event):
        if self.debug:
            logger.debug(f"Event detected: {event}")
        if event.is_directory:
            logger.info(f"New directory created: {event.src_path}")
            dest_path = f"{self.destination}/{event.src_path.split('/')[-1]}"
            try:
                shutil.copytree(event.src_path, dest_path)
                logger.info(f"Copied {event.src_path} to {dest_path}")
            except Exception as e:
                logger.error(f"Failed to copy {event.src_path} to {dest_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Watch a directory for new subdirectory creation and copy it to a destination."
    )
    parser.add_argument(
        "--source",
        type=str,
        default=os.getenv("SOURCE_DIR", "/watchsrc"),
        help="The source directory to watch for new subdirectories. Default is '/watchsrc' or the value of the SOURCE_DIR environment variable.",
    )
    parser.add_argument(
        "--destination",
        type=str,
        default=os.getenv("DESTINATION_DIR", "/watchdst"),
        help="The destination directory where new subdirectories will be copied. Default is '/watchdst' or the value of the DESTINATION_DIR environment variable.",
    )
    parser.add_argument(
        "--recursive",
        type=bool,
        default=os.getenv("RECURSIVE", "true").lower() == "true",
        help="Set to True to watch subdirectories recursively, or False to watch only the top-level directory. Default is True or the value of the RECURSIVE environment variable.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.getenv("DEBUG", "false").lower() == "true",
        help="Enable debug mode to print detailed logs. Default is False or the value of the DEBUG environment variable.",
    )
    parser.add_argument(
        "--sleep-time",
        type=float,
        default=float(os.getenv("SLEEP_TIME", 10)),
        help="The time (in seconds) to sleep between observer checks. Default is 1.0 seconds or the value of the SLEEP_TIME environment variable.",
    )
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    source_path = args.source
    destination_path = args.destination
    recursive = args.recursive
    sleep_time = args.sleep_time

    event_handler = DirectoryCreationHandler(destination_path, debug=args.debug)
    observer = Observer()
    observer.schedule(event_handler, path=source_path, recursive=recursive)

    logger.info(f"Watching for new directories in: {source_path}")
    logger.info(f"New directories will be copied to: {destination_path}")
    logger.info(f"Recursive watching is set to: {recursive}")
    logger.info(f"Observer sleep time is set to: {sleep_time} seconds")
    try:
        observer.start()
        while True:
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopped watching.")
    observer.join()


if __name__ == "__main__":
    main()
