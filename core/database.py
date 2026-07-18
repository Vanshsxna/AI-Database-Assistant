"""
core/database.py

Core Database class for the Mini Database Engine.
"""

from pathlib import Path
from typing import Any, Dict, List

from .storage import Storage
from .table import Table


class Database:
    """
    Main database manager.

    Responsibilities:
    - Load/save database
    - Create/drop tables
    - Return table objects
    """

    def __init__(self, db_file: str = "data/database.json") -> None:
        self.db_file = Path(db_file)
        self.storage = Storage(self.db_file)
        self.tables: Dict[str, Table] = {}

        self._load()

    def _load(self) -> None:
        raw = self.storage.load()

        self.tables = {}

        for table_name, table_data in raw.items():
            self.tables[table_name] = Table.from_dict(table_data)

    def save(self) -> None:
        data = {
            name: table.to_dict()
            for name, table in self.tables.items()
        }
        self.storage.save(data)

    def create_table(self, name: str, columns: List[str]) -> None:
        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists.")

        self.tables[name] = Table(name=name, columns=columns)
        self.save()

    def drop_table(self, name: str) -> None:
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist.")

        del self.tables[name]
        self.save()

    def list_tables(self) -> List[str]:
        return sorted(self.tables.keys())

    def table_exists(self, name: str) -> bool:
        return name in self.tables

    def get_table(self, name: str) -> Table:
        if name not in self.tables:
            raise ValueError(f"Table '{name}' does not exist.")
        return self.tables[name]

    def insert(self, table: str, row: Dict[str, Any]) -> None:
        self.get_table(table).insert(row)
        self.save()

    def select(
        self,
        table: str,
        where=None,
        order_by=None,
        reverse: bool = False,
        limit: int | None = None,
    ):
        return self.get_table(table).select(
            where=where,
            order_by=order_by,
            reverse=reverse,
            limit=limit,
        )

    def update(self, table: str, values: Dict[str, Any], where=None) -> int:
        count = self.get_table(table).update(values, where)
        self.save()
        return count

    def delete(self, table: str, where=None) -> int:
        count = self.get_table(table).delete(where)
        self.save()
        return count

    def count(self, table: str, where=None) -> int:
        return self.get_table(table).count(where)

    def truncate(self, table: str) -> None:
        self.get_table(table).truncate()
        self.save()

    def export(self) -> Dict[str, Any]:
        return {
            name: table.to_dict()
            for name, table in self.tables.items()
        }

    def __contains__(self, item: str) -> bool:
        return item in self.tables

    def __len__(self) -> int:
        return len(self.tables)

    def __repr__(self) -> str:
        return f"Database(tables={self.list_tables()})"
