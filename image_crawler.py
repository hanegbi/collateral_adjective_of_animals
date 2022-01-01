import asyncio
import os
from logging import Logger
from typing import List, Optional

import httpx
import requests
from bs4 import BeautifulSoup

from animal import Animal
from consts import (
    BASE_WIKIPEDIA_URL,
    HTML_PARSER,
    TABLE,
    INFOBOX_BIOTA,
    IMG,
    SRC,
    HTTP,
    IMAGES_FOLDER,
    TIMEOUT_ERROR_MESSAGE,
    UNEXPECTED_ERROR_ERROR_MESSAGE,
    THERE_IS_NO_IMAGE,
    DOWNLOADED_ANIMAL_IMAGE,
    TMP_FOLDER,
    ANIMAL_IMAGE_FILE,
    ANIMAL_IMAGE_ALREADY_EXISTS,
    HTTPX_GET_TIMEOUT,
)


class ImageCrawler:
    """
    Crawl over Wikipedia pages of animals and download their image from infobox on page.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    async def save_images(self, animals: List[Animal]):
        """
        Create list of coroutines of save_image and the save all images asynchronously.

        :param animals: List of all animals created on WikipediaAnimalsApi.
        """
        tasks = []
        for animal in animals:
            if not self._is_animal_image_exist(animal.name):
                tasks.append(self.save_image(animal))
            else:
                self.logger.info(ANIMAL_IMAGE_ALREADY_EXISTS.format(animal_name=animal.name))

        await asyncio.gather(*tasks)

    async def save_image(self, animal: Animal):
        """
        Get image source and then download it.

        :param animal: Animal object with data.
        """
        img_url = await self.get_image_src(animal)

        self._create_images_folder()
        self._write_animal_image(img_url, animal.name)

    async def get_image_src(self, animal: Animal) -> Optional[str]:
        """
        Get image source on infobox from Wikipedia page of the animal.

        :param animal: Animal object with data.

        :return: Image source of the animal.
        """
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(BASE_WIKIPEDIA_URL + animal.href, timeout=HTTPX_GET_TIMEOUT)
                soup = BeautifulSoup(res.content, HTML_PARSER)
                infobox = soup.find(TABLE, class_=INFOBOX_BIOTA)
            try:
                img = infobox.find(IMG)[SRC]
            except AttributeError:
                self.logger.error(THERE_IS_NO_IMAGE.format(animal_name=animal.name))
                return None
        except httpx.TimeoutException:
            self.logger.error(TIMEOUT_ERROR_MESSAGE.format(animal_name=animal.name))
            return None
        except httpx.RequestError as e:
            self.logger.error(UNEXPECTED_ERROR_ERROR_MESSAGE.format(e=e, animal_name=animal.name))
            return None

        return img

    def _create_images_folder(self):
        """
        Create tmp folder and images folders if they are not exist.
        """
        if not os.path.exists(TMP_FOLDER):
            os.makedirs(TMP_FOLDER)
        if not os.path.exists(f"{TMP_FOLDER}/{IMAGES_FOLDER}"):
            os.makedirs(f"{TMP_FOLDER}/{IMAGES_FOLDER}")

    def _write_animal_image(self, img_url: str, animal_name: str):
        """
        Download animal image from given image source.

        :param img_url: Image source of the animal.
        :param animal_name: Name of the animal.
        """
        if img_url:
            with open(f"{TMP_FOLDER}/{IMAGES_FOLDER}/{ANIMAL_IMAGE_FILE.format(animal_name=animal_name)}", "wb") as f:
                f.write(requests.get(HTTP + img_url).content)
            self.logger.info(DOWNLOADED_ANIMAL_IMAGE.format(animal_name=animal_name))

    def _is_animal_image_exist(self, animal_name: str) -> bool:
        """
        Check if image of animal is already exists.

        :param animal_name: Name of the animal.

        :return: True if image exists otherwise False.
        """
        return os.path.isfile(
            os.path.abspath(f"{TMP_FOLDER}/{IMAGES_FOLDER}/{ANIMAL_IMAGE_FILE.format(animal_name=animal_name)}")
        )
