import asyncio
import subprocess
import sys

from consts import PRODUCE_IS_DONE
from wiki_logger import WikiLogger
from image_crawler import ImageCrawler
from wikipedia_animals_api import WikipediaAnimalsApi


def run():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"])

    logger = WikiLogger().get_logger()

    wa = WikipediaAnimalsApi(logger=logger)
    wa.produce_collateral_adjectives_to_animals()

    animals = wa.get_animals()
    ic = ImageCrawler(logger=logger)
    asyncio.get_event_loop().run_until_complete(ic.save_images(animals))

    logger.info(PRODUCE_IS_DONE)


if __name__ == "__main__":
    run()
