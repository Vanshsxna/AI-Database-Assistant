from core.database import Database
from ai.schemas import Command


class UnsupportedActionError(Exception):
    pass


class Executor:

    def __init__(self, db: Database):
        self.db = db

        self.actions = {
            "create": self._create,
            "insert": self._insert,
            "select": self._select,
            "update": self._update,
            "delete": self._delete,
            "count": self._count,
            "tables": self._tables,
            "info": self._info,
            "truncate": self._truncate,
            "drop": self._drop,
        }

    def execute(self, command: Command):
        action = (command.action or "").lower()

        handler = self.actions.get(action)

        if handler is None:
            raise UnsupportedActionError(
                f"Unsupported action: {command.action}"
            )

        return handler(command)

    def _create(self, command: Command):
        self._require(command, "table")
        self._require(command, "columns")

        return self.db.create_table(
            command.table,
            command.columns
        )

    def _insert(self, command: Command):
        self._require(command, "table")
        self._require(command, "values")

        return self.db.insert(
            command.table,
            command.values
        )

    def _select(self, command: Command):
        self._require(command, "table")

        return self.db.select(
            command.table,
            where=command.where,
            order_by=command.order_by,
            reverse=bool(command.reverse),
            limit=command.limit
        )

    def _update(self, command: Command):
        self._require(command, "table")
        self._require(command, "values")

        if command.where is None:
            raise ValueError(
                "UPDATE requires a WHERE clause."
            )

        return self.db.update(
            command.table,
            command.values,
            where=command.where
        )

    def _delete(self, command: Command):
        self._require(command, "table")

        if command.where is None:
            raise ValueError(
                "DELETE requires a WHERE clause."
            )

        return self.db.delete(
            command.table,
            where=command.where
        )

    def _count(self, command: Command):
        self._require(command, "table")

        return self.db.count(
            command.table,
            where=command.where
        )

    def _tables(self, command: Command):
        tables = self.db.list_tables()

        return {
            "success": True,
            "message": f"{len(tables)} table(s) found.",
            "data": tables
        }

    def _info(self, command: Command):
        self._require(command, "table")

        return self.db.table_info(
            command.table
        )

    def _truncate(self, command: Command):
        self._require(command, "table")

        return self.db.truncate(
            command.table
        )

    def _drop(self, command: Command):
        self._require(command, "table")

        return self.db.drop_table(
            command.table
        )
    
    def _require(self, command: Command, field: str):
        value = getattr(command, field, None)

        if value in (None, {}, []):
            raise ValueError(
                f"'{command.action}' requires a valid '{field}' field."
            )