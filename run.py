import asyncio

from consts import PRODUCE_IS_DONE
from wiki_logger import WikiLogger
from image_crawler import ImageCrawler
from wikipedia_animals_api import WikipediaAnimalsApi

if __name__ == "__main__":
    logger = WikiLogger().get_logger()

    wa = WikipediaAnimalsApi(logger=logger)
    wa.produce_collateral_adjectives_to_animals()

    animals = wa.get_animals()
    ic = ImageCrawler(logger=logger)
    asyncio.get_event_loop().run_until_complete(ic.save_images(animals))

    logger.info(PRODUCE_IS_DONE)
