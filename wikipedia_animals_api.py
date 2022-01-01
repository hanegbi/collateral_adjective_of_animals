import pprint
import re
from collections import defaultdict
from logging import Logger

import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional

from animal import Animal
from consts import (
    BASE_WIKIPEDIA_URL,
    LIST_OF_ANIMAL_NAMES_URL,
    TIMEOUT_ERROR_MESSAGE,
    UNEXPECTED_ERROR_ERROR_MESSAGE,
    HTML_PARSER,
    TABLE,
    WIKITABLE,
    INDEX_TERMS_BY_SPECIES_OR_TAXON_TABLE,
    TR,
    QUESTION_MARK,
    INSIDE_SQUARE_BRACKETS,
    EMPTY_STR,
    BR,
    TITLE_AND_HREF_INDEX,
    ANCHOR,
    TITLE,
    COLLATERAL_ADJECTIVE,
    HREF,
    INSIDE_ROUND_BRACKETS,
    TD,
    PARING_TABLE_TERMS_BY_SPECIES_OR_TAXON,
    GOT_ANIMAL_DATA,
)


class WikipediaAnimalsApi:
    """
    Create correlation between collateral adjectives to animals from List_of_animal_names on Wikipedia.
    """

    def __init__(self, logger: Logger):
        self.animals: List[Animal] = []
        self.logger = logger

    def get_animals(self) -> List[Animal]:
        """
        Get list of animals.

        :return: List of animals.
        """
        return self.animals

    def produce_collateral_adjectives_to_animals(self):
        """
        Producing a map and then print it of collateral adjectives of animals from List_of_animal_names on Wikipedia.
        """
        content = self._get_wikipedia_page_content()
        if content is None:
            return None

        table_rows = self._parse_table_rows(content)

        for row in table_rows:
            self._create_animal_data(row)

        col_adj_map = self._produce_collateral_adjectives_map()
        pprint.pprint(col_adj_map)

    def _produce_collateral_adjectives_map(self) -> Dict[str, List[str]]:
        """
        Produce collateral adjectives map from Animals objects

        :return: Dict of collateral_adjective as key and list of animals as value.
        """
        col_adj_map = defaultdict(list)
        for animal in self.animals:
            for col_adj in animal.collateral_adjectives:
                col_adj_map[col_adj].append(animal)

        return col_adj_map

    def _get_wikipedia_page_content(self) -> Optional[str]:
        """
        Get request for List_of_animal_names from Wikipedia and returns its content.

        :return: Content of the Wikipedia page.
        """
        try:
            res = requests.get(url=BASE_WIKIPEDIA_URL + LIST_OF_ANIMAL_NAMES_URL)
        except requests.exceptions.Timeout:
            self.logger.error(TIMEOUT_ERROR_MESSAGE)
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(UNEXPECTED_ERROR_ERROR_MESSAGE.format(e=e))
            return None

        return res.text

    def _parse_table_rows(self, content: str) -> list:
        """
        Get a list of table rows of "Terms by species or taxon".

        :param content: Content of List_of_animal_names Wikipedia page.

        :return: Rows of table "Terms by species or taxon".
        """
        self.logger.info(PARING_TABLE_TERMS_BY_SPECIES_OR_TAXON)
        soup = BeautifulSoup(content, HTML_PARSER)
        table = soup.find_all(TABLE, class_=WIKITABLE)[INDEX_TERMS_BY_SPECIES_OR_TAXON_TABLE]
        return table.find_all(TR)

    def _handle_collateral_adjective_cell(self, collateral_adjective_cell: Tag) -> list:
        """
        Create a list of collateral adjectives from the data cell.

        :param collateral_adjective_cell: Table data cell of collateral adjective columns.

        :return: List of collateral adjectives of the animal.
        """
        collateral_adjective_cell = collateral_adjective_cell.get_text(separator=BR)
        collateral_adjective_cell = re.sub(INSIDE_SQUARE_BRACKETS, EMPTY_STR, collateral_adjective_cell)

        if collateral_adjective_cell == QUESTION_MARK:
            return []
        else:
            collateral_adjectives = [
                col_adj.strip().lower() for col_adj in collateral_adjective_cell.split(BR) if col_adj
            ]
            return collateral_adjectives

    def _create_animal_data(self, row: Tag) -> Animal:
        """
        Create animal and set data.

        :param row: Row with data of animal of table "Terms by species or taxon"

        :return: Animal with data.
        """
        table_data_cell = row.find_all(TD)
        if table_data_cell:
            animal = Animal(
                name=re.sub(
                    INSIDE_ROUND_BRACKETS, EMPTY_STR, table_data_cell[TITLE_AND_HREF_INDEX].find(ANCHOR)[TITLE]
                ),
                href=table_data_cell[TITLE_AND_HREF_INDEX].find(ANCHOR)[HREF],
                collateral_adjectives=self._handle_collateral_adjective_cell(table_data_cell[COLLATERAL_ADJECTIVE]),
            )
            self.animals.append(animal)
            self.logger.info(GOT_ANIMAL_DATA.format(animal_name=animal.name))
            return animal
