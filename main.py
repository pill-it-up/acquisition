from picamera import PiCamera
from pathlib import Path
from argparse import ArgumentParser

import logging

logging.basicConfig(
    filename="{}".format(Path("~") / "logs" / "acquisition.log"),
    format="%(asctime)s == PILLITUP == BACKEND == [%(levelname)-8s] %(message)s",
)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("pill", help="pill name")
    parser.add_argument("amount", help="how many pictures", type=int)

    return parser.parse_args()


def main():
    args = get_args()

    logging.info("Starting acquisition for {} {} times.".format(args.pill, args.amount))

    current_dir = Path(".")
    dataset_dir = current_dir / "dataset"

    if not dataset_dir.exists():
        logging.debug("dataset directory doesn't exist, creating...")
        dataset_dir.mkdir()

    with PiCamera() as cam:
        logging.info("Starting camera live preview.")
        cam.start_preview()

        logging.info("Starting camera sequence capture.")
        cam.capture_sequence(
            [
                "{}".format(dataset_dir / "{}_{}.jpg".format(args.pill, i))
                for i in range(args.amount)
            ]
        )
        logging.info("Sequence capture done.")

        logging.info("Stopping camera live preview.")
        cam.stop_preview()

        logging.info("Done.")


if __name__ == "__main__":
    main()
