import pytest

from image_crawler import ImageCrawler
from test.consts import VALID_ANIMAL, IMG_SUFFIX, ANIMAL_WITHOUT_IMAGE
from wiki_logger import WikiLogger


@pytest.mark.asyncio
class TestImageCrawler:
    """
    Test for ImageCrawler functionality.
    """

    @pytest.fixture()
    def image_crawler(self):
        """
        Init ImageCrawler with a logger.
        """
        image_crawler = ImageCrawler(logger=WikiLogger().get_logger())
        yield image_crawler

    async def test_get_image_src_happy_flow(self, image_crawler):
        """
        Get image source of animal.
        Assert the source is an image.
        """
        image_src = await image_crawler.get_image_src(VALID_ANIMAL)
        assert self.is_image(image_src)

    async def test_get_image_src_animal_without_image(self, image_crawler):
        """
        Get image source of Animal does not have image on infobox.
        Assert get_image_src returned None.
        """
        image_src = await image_crawler.get_image_src(ANIMAL_WITHOUT_IMAGE)
        assert image_src is None

    @staticmethod
    def is_image(image_src: str):
        return image_src.lower().endswith(IMG_SUFFIX)
