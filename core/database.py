from .storage import Storage
from .schema import Schema
from .constraints import Constraints
from .validator import Validator
from copy import deepcopy


class Database:
    def __init__(self, filename="data/mydb.json"):
        self.filename = filename
        self.tables = {}
        self._load()

    def _load(self):
        self.tables = Storage.load(self.filename)

    def save(self):
        Storage.save(
            self.filename,
            self.tables
        )

    def _result(
        self,
        success,
        message,
        data=None
    ):

        return {
            "success": success,
            "message": message,
            "data": data
        }

    def _get_table(self, table_name):
        return self.tables.get(table_name)

    def table_exists(self, table_name):
        return table_name in self.tables

    def list_tables(self):
        return sorted(self.tables.keys())

    def export(self):
        return deepcopy(self.tables)

    def __contains__(self, table_name):
        return table_name in self.tables

    def __len__(self):
        return len(self.tables)

    def __repr__(self):
        return (
            f"Database("
            f"tables={len(self.tables)}, "
            f"filename='{self.filename}')"
        )

    def create_table(self, table_name, columns):
        if self.table_exists(table_name):
            return self._result(
                False,
                f"Table '{table_name}' already exists."
            )

        success, schema = Schema.build(columns)

        if not success:
            return self._result(False, schema)

        self.tables[table_name] = {
            "schema": schema,
            "rows": []
        }

        self.save()

        return self._result(
            True,
            f"Table '{table_name}' created successfully."
        )

    def drop_table(self, table_name):
        table = self._get_table(table_name)

        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        del self.tables[table_name]

        self.save()

        return self._result(
            True,
            f"Table '{table_name}' deleted successfully."
        )

    def insert(self, table_name, row):
        table = self._get_table(table_name)
        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        success, validated_row = Constraints.validate(
            table,
            row
        )

        if not success:
            return self._result(
                False,
                validated_row
            )

        table["rows"].append(validated_row)

        self.save()

        return self._result(
            True,
            "Row inserted successfully.",
            validated_row
        )

    def _evaluate_condition(self, row, where):
        if where is None:
            return True

        if len(where) != 3:
            return False

        column, operator, value = where
        if column not in row:
            return False

        current = row[column]

        try:

            if operator == "==":
                return current == value

            elif operator == "!=":
                return current != value

            elif operator == ">":
                return current > value

            elif operator == "<":
                return current < value

            elif operator == ">=":
                return current >= value

            elif operator == "<=":
                return current <= value

            else:
                return False

        except Exception:
            return False

    def select(
        self,
        table_name,
        where=None,
        order_by=None,
        reverse=False,
        limit=None
    ):

        table = self._get_table(table_name)
        if table is None:

            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        rows = table["rows"][:]

        if where is not None:
            rows = [
                row
                for row in rows
                if self._evaluate_condition(
                    row,
                    where
                )
            ]

        if order_by is not None:
            if order_by not in table["schema"]:
                return self._result(
                    False,
                    f"Unknown column '{order_by}'."
                )

            rows.sort(
                key=lambda row: row[order_by],
                reverse=reverse
            )

        if limit is not None:
            rows = rows[:limit]
        return self._result(
            True,
            "Query executed successfully.",
            rows
        )

    def count(
        self,
        table_name,
        where=None
    ):

        result = self.select(
            table_name,
            where=where
        )

        if not result["success"]:
            return result

        return self._result(
            True,
            "Count successful.",
            len(result["data"])
        )

    def update(
        self,
        table_name,
        values,
        where=None
    ):

        table = self._get_table(table_name)
        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        schema = table["schema"]
        rows = table["rows"]

        for column in values:
            if column not in schema:
                return self._result(
                    False,
                    f"Unknown column '{column}'."
                )

        updated = 0

        for row in rows:
            if not self._evaluate_condition(row, where):
                continue

            new_row = row.copy()

            for column, value in values.items():
                success, converted = Validator.validate(
                    value,
                    schema[column]["type"]
                )

                if not success:
                    return self._result(False, converted)

                new_row[column] = converted

            # UNIQUE / PRIMARY KEY check
            for column, info in schema.items():

                constraints = info["constraints"]

                if constraints["primary_key"] or constraints["unique"]:

                    new_value = new_row[column]

                    # Nulls are never considered duplicates of each other.
                    if new_value is None:
                        continue

                    for existing in rows:

                        if existing is row:
                            continue

                        if existing[column] == new_value:

                            return self._result(
                                False,
                                f"Duplicate value '{new_value}' in column '{column}'."
                            )

            row.update(new_row)

            updated += 1

        self.save()

        return self._result(
            True,
            f"{updated} row(s) updated.",
            {
                "updated": updated
            }
        )

    def delete(
        self,
        table_name,
        where=None
    ):
        table = self._get_table(table_name)
        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        rows = table["rows"]
        original = len(rows)
        table["rows"] = [
            row
            for row in rows
            if not self._evaluate_condition(
                row,
                where
            )

        ]
        deleted = original - len(table["rows"])
        self.save()
        return self._result(
            True,
            f"{deleted} row(s) deleted.",
            deleted
        )

    def truncate(
        self,
        table_name
    ):
        table = self._get_table(table_name)
        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )
        deleted = len(table["rows"])
        table["rows"] = []
        self.save()
        return self._result(
            True,
            f"{deleted} row(s) removed."
        )

    def table_info(self, table_name):
        table = self._get_table(table_name)

        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        return self._result(
            True,
            "Schema fetched successfully.",
            table["schema"]
        )

    def clear_database(self):
        self.tables = {}
        self.save()

        return self._result(
            True,
            "Database cleared successfully."
        )

    def rename_table(
        self,
        old_name,
        new_name
    ):

        if old_name not in self.tables:

            return self._result(
                False,
                f"Table '{old_name}' does not exist."
            )

        if new_name in self.tables:

            return self._result(
                False,
                f"Table '{new_name}' already exists."
            )

        self.tables[new_name] = self.tables.pop(old_name)

        self.save()

        return self._result(
            True,
            "Table renamed successfully."
        )