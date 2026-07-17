from database import Database

db = Database("mydb.json")

print("Hello, Vanshh")
print("Type HELP to see commands, EXIT to quit\n")


def display_result(result):

    print(result["message"])

    if result["success"] and result["data"]:

        data = result["data"]

        if "columns" in data:
            print(data["columns"])

        if "rows" in data:
            for row in data["rows"]:
                print(row)


while True:

    command = input("DB> ").strip()

    if not command:
        continue

    parts = command.split()

    if parts[0].upper() == "EXIT":
        print("Exiting Database...")
        break

    elif parts[0].upper() == "HELP":
        print("""
Commands

CREATE students id name marks

INSERT students 1 Vansh 95

SELECT students

SELECT students marks > 80

UPDATE students marks 98 WHERE id == 1

DELETE students marks < 40

EXIT
""")

    # -----------------------------
    # CREATE
    # -----------------------------

    elif parts[0].upper() == "CREATE":

        table_name = parts[1]
        columns = parts[2:]

        result = db.create_table(
            table_name,
            columns
        )

        display_result(result)

    # -----------------------------
    # INSERT
    # -----------------------------

    elif parts[0].upper() == "INSERT":

        table_name = parts[1]

        values = []

        for value in parts[2:]:

            if value.isdigit():
                values.append(int(value))
            else:
                values.append(value)

        result = db.insert_row(
            table_name,
            values
        )

        display_result(result)

    # -----------------------------
    # SELECT
    # -----------------------------

    elif parts[0].upper() == "SELECT":

        table_name = parts[1]

        if len(parts) == 2:

            result = db.select_all(
                table_name
            )

        else:

            column = parts[2]
            operator = parts[3]

            value = parts[4]

            if value.isdigit():
                value = int(value)

            result = db.select_where(
                table_name,
                column,
                operator,
                value
            )

        display_result(result)

    # -----------------------------
    # UPDATE
    # -----------------------------

    elif parts[0].upper() == "UPDATE":

        table_name = parts[1]

        set_column = parts[2]

        new_value = parts[3]

        if new_value.isdigit():
            new_value = int(new_value)

        where_column = parts[5]

        operator = parts[6]

        where_value = parts[7]

        if where_value.isdigit():
            where_value = int(where_value)

        result = db.update_where(
            table_name,
            set_column,
            new_value,
            where_column,
            operator,
            where_value
        )

        display_result(result)

    # -----------------------------
    # DELETE
    # -----------------------------

    elif parts[0].upper() == "DELETE":

        table_name = parts[1]

        column = parts[2]

        operator = parts[3]

        value = parts[4]

        if value.isdigit():
            value = int(value)

        result = db.delete_where(
            table_name,
            column,
            operator,
            value
        )

        display_result(result)

    else:
        print("Unknown command.")