from picamera import PiCamera
from pathlib import Path
from argparse import ArgumentParser

import time
import logging

logging.basicConfig(
    filename="{}".format(Path.home() / "logs" / "acquisition.log"),
    format="%(asctime)s == PILLITUP == ACQUISITION == [%(levelname)-8s] %(message)s",
    level=logging.DEBUG,
)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("pill", help="pill name")
    parser.add_argument("amount", help="how many pictures", type=int)

    return parser.parse_args()


def main():
    args = get_args()

    logging.info("Starting acquisition for {} {} times.".format(args.pill, 200))

    current_dir = Path(".")
    dataset_dir = current_dir / "dataset"

    if not dataset_dir.exists():
        logging.debug("dataset directory doesn't exist, creating...")
        dataset_dir.mkdir()

    pill_dir = dataset_dir / args.pill

    if not pill_dir.exists():
        logging.debug("pill directory doesn't exist, creating...")
        pill_dir.mkdir()

    with PiCamera() as cam:
        logging.info("Starting camera live preview.")
        cam.start_preview()

        logging.info("Starting camera sequence capture.")
        cam.capture_sequence(
            [
                "{}".format(pill_dir / "{:d}_{}.jpg".format(int(time.time()), i))
                for i in range(args.amount)
            ]
        )
        logging.info("Sequence capture done.")

        logging.info("Stopping camera live preview.")
        cam.stop_preview()

        logging.info("Done.")


if __name__ == "__main__":
    main()
