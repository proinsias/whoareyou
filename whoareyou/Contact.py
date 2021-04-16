# -*- coding: utf-8 -*-
import dataclasses
import typing


@dataclasses.dataclass
class Contact:
    first_name: str
    surname: str
    photo_data: typing.Optional[str]
