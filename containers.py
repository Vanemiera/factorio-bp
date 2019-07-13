@dataclass
class Blueprint():
    item: str
    label: str
    version: int
    icons: list
    entities: list
    tiles: list


@dataclass
class BlueprintBook():
    pass

@dataclass
class Position():
    x: float
    y:float

@dataclass
class Entity():
    entity_number: int
    name: str
    position: Position
    direction: int
    

@dataclass
class ControlBehaviour():
    pass

@dataclass
class CircuitCondition():
    pass

@dataclass
class Connection():
    pass
    #points: List[ConnectionPoint]

@dataclass
class Icon():
    pass

@dataclass
class Tile():
    pass

@dataclass
class SignalID():
    name: str
    type: str

@dataclass
class ConnectionData():
    entity_id: int
    circuit_id: int

@dataclass
class ConnectionPoint():
    red: ConnectionData
    green: ConnectionData

@dataclass
class ItemRequest():
    items: dict

@dataclass
class ItemFilter():
    name: str
    index: int

@dataclass
class Color():
    r: float
    g: float
    b: float
    a: float

@dataclass
class SpeakerParameter():
    playback_volume: float
    playback_globally: bool
    allow_polyphony: bool

@dataclass
class SpeakerAlertParameter():
    show_alert: bool
    show_on_map: bool
    icon_signal_id: SignalID
    alert_message: str

@dataclass
class LogisticFilter():
    name: str
    index: int
    count: int

class FactorioBPEncoder(json.JSONEncoder):
    pass

class FactorioBPDecoder(json.JSONDecoder):
    pass