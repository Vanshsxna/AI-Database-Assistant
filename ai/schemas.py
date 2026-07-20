from dataclasses import dataclass, field

@dataclass
class Command:

    action: str = ""

    table: str = ""

    values: dict[str, object] = field(default_factory=dict)

    columns: list[str] = field(default_factory=list)

    where: dict | None = None

    order_by: str | None = None

    reverse: bool = False

    limit: int | None = None