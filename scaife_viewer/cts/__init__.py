from .capitains import default_resolver  # noqa
from .exceptions import PassageDoesNotExist
from .collections import (  # noqa
    TextInventory,
    Collection,
    TextGroup,
    Work,
    Text,
    resolve_collection,
)
from .passage import Passage
from .reference import URN


def text_inventory() -> TextInventory:
    return TextInventory.load()


def collection(urn: str) -> Collection:
    metadata = TextInventory.load().metadata[urn]
    return resolve_collection(metadata.TYPE_URI)(URN(urn), metadata)


def passage(urn: str) -> Passage:
    urn = URN(urn)
    if urn.reference is None:
        reference = None
        text = collection(str(urn))
        if not isinstance(text, Text):
            raise ValueError("urn must be a text or contain a reference")
    else:
        reference = urn.reference
        urn = urn.upTo(URN.NO_PASSAGE)
        text = collection(urn)
    passage = Passage(text, reference=reference)
    if not passage.exists():
        raise PassageDoesNotExist(text, f"{reference} does not exist in {urn}")
    return passage
