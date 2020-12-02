# enumerate a enum
def listEnum(enum):
    return list(map(lambda _: str(_.value), enum))
