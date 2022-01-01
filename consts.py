BASE_WIKIPEDIA_URL = "https://en.wikipedia.org"
LIST_OF_ANIMAL_NAMES_URL = "/wiki/List_of_animal_names"

TABLE = "table"
WIKITABLE = "wikitable"
INFOBOX_BIOTA = "infobox biota"
HTML_PARSER = "html.parser"
HTTP = "http:"
TMP_FOLDER = "tmp"
IMAGES_FOLDER = "images"
ANIMAL_IMAGE_FILE = "{animal_name}.jpg"

TR = "tr"
TD = "td"
ANCHOR = "a"
TITLE = "title"
HREF = "href"
IMG = "img"
SRC = "src"
EMPTY_STR = ""
QUESTION_MARK = "?"
BR = "<br/>"

INSIDE_ROUND_BRACKETS = r"\(.*?\)"
INSIDE_SQUARE_BRACKETS = r"\[.*?\]"

TITLE_AND_HREF_INDEX = 0
INDEX_TERMS_BY_SPECIES_OR_TAXON_TABLE = 1
COLLATERAL_ADJECTIVE = 5

HTTPX_GET_TIMEOUT = 60

TIMEOUT_ERROR_MESSAGE = "Failed to retrieve site due to timeout error of {animal_name}"
UNEXPECTED_ERROR_ERROR_MESSAGE = "Failed to retrieve site due to unexpected error: {e} of {animal_name}"
PARING_TABLE_TERMS_BY_SPECIES_OR_TAXON = "Paring table Terms by species or taxon"
GOT_ANIMAL_DATA = "Finish getting data of {animal_name}"
DOWNLOADED_ANIMAL_IMAGE = "Finish download image of {animal_name}"
THERE_IS_NO_IMAGE = "There is no image of {animal_name}"
ANIMAL_IMAGE_ALREADY_EXISTS = "Image of {animal_name} is already exists"
PRODUCE_IS_DONE = "Producing collateral adjectives for animals is DONE"

LOGGER_FORMAT = "[%(asctime)s] %(levelname)s - %(message)s"
LOGGER_FILENAME = "logger.log"
