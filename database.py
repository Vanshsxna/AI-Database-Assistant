import json
import os

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.tables = {}

        if os.path.exists(self.filename):
            self.load()
        else:
            self.save()

    # Helper Methods

    def _result(self, success, message, data=None):
        return {
            "success": success,
            "message": message,
            "data": data
        }

    def _get_table(self, table_name):
        return self.tables.get(table_name)

    # def _get_column_index(self, table, column):
    #     if column not in table["columns"]:
    #         return None
    #     return table["columns"].index(column)

    def _evaluate_condition(self, cell_value, operator, target_value):
        if operator == ">":
            return cell_value > target_value

        elif operator == "<":
            return cell_value < target_value

        elif operator == "==":
            return cell_value == target_value

        else:
            return False
        
    # Storage

    def save(self):

        with open(self.filename, "w") as file:
            json.dump(self.tables, file, indent=4)

    def load(self):
        """
        Load the database from a JSON file.
        """

        with open(self.filename, "r") as file:
            self.tables = json.load(file)
        

    # Table Operations

    def create_table(self, table_name, columns):
        if self._get_table(table_name):
            return self._result(
                False,
                f"Table '{table_name}' already exists."
            )

        self.tables[table_name] = {
            "columns": columns,
            "rows": []
        }

        self.save()

        return self._result(
            True,
            f"Table '{table_name}' created successfully."
        )

    def insert_row(self, table_name, values):
        table = self._get_table(table_name)

        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        if len(values) != len(table["columns"]):
            return self._result(
                False,
                "Column count does not match the number of values."                
            )

        row = dict(zip(table["columns"], values))
        table["rows"].append(row)

        self.save()

        return self._result(
            True,
            f"Row inserted into '{table_name}'."
        )
    
    # Select Operations

    def select_all(self, table_name):
        table = self._get_table(table_name)

        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        return self._result(
            True,
            f"{len(table['rows'])} record(s) found.",
            {
                "columns": table["columns"],
                "rows": table["rows"]
            }
        )

    def select_where(self, table_name, column, operator, value):
        table = self._get_table(table_name)

        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        if column not in table["columns"]:
            return self._result(
               False,
               f"Column '{column}' does not exist."
    )

        matching_rows = []

        for row in table["rows"]:

            cell_value = row[column]

            if self._evaluate_condition(
                cell_value,
                operator,
                value
            ):
                matching_rows.append(row)

        return self._result(
            True,
            f"{len(matching_rows)} record(s) found.",
            {
                "columns": table["columns"],
                "rows": matching_rows
            }
        )

    # Update Operations

    def update_where(
        self,
        table_name,
        set_column,
        new_value,
        where_column,
        operator,
        where_value
    ):

        table = self._get_table(table_name)

        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        if set_column not in table["columns"]:
         return self._result(
            False,
            f"Column '{set_column}' does not exist."
    )

        if where_column not in table["columns"]:
            return self._result(
                False,
                f"Column '{where_column}' does not exist."
    )

        updated_rows = 0

        for row in table["rows"]:

            cell_value = row[where_column]

            if self._evaluate_condition(
                cell_value,
                operator,
                where_value
            ):
                row[set_column] = new_value
                updated_rows += 1

        self.save()

        return self._result(
            True,
            f"{updated_rows} row(s) updated."
        )

    # Delete Operations

    def delete_where(
        self,
        table_name,
        column,
        operator,
        value
    ):

        table = self._get_table(table_name)

        if table is None:
            return self._result(
                False,
                f"Table '{table_name}' does not exist."
            )

        if column not in table["columns"]:
            return self._result(
               False,
               f"Column '{column}' does not exist."
    )

        remaining_rows = []

        deleted_rows = 0

        for row in table["rows"]:

            cell_value = row[column]

            if self._evaluate_condition(
                cell_value,
                operator,
                value
            ):
                deleted_rows += 1

            else:
                remaining_rows.append(row)

        table["rows"] = remaining_rows

        self.save()

        return self._result(
            True,
            f"{deleted_rows} row(s) deleted."
        )