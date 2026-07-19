from core.database import Database

db = Database("data/mydb.json")

print("Hello, Vanshh")
print("Type HELP to see commands, EXIT to quit\n")


def display_result(result):
    print(result["message"])

    if not result["success"]:
        return

    data = result["data"]

    if isinstance(data, list):
        for row in data:
            print(row)

    elif isinstance(data, dict):
        print(data)


def coerce(value):

    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def parse_kv_pairs(tokens):

    row = {}

    for token in tokens:
        if "=" not in token:
            print(f"Ignoring malformed argument '{token}' (expected column=value).")
            continue

        column, value = token.split("=", 1)
        row[column] = value

    return row


def parse_where(tokens):

    if not tokens:
        return None

    if tokens[0].upper() != "WHERE":
        print("Expected WHERE clause.")
        return None

    if len(tokens) < 4:
        print("Malformed WHERE clause. Expected: WHERE column operator value")
        return None

    column, operator, value = tokens[1], tokens[2], tokens[3]
    return (column, operator, coerce(value))


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

CREATE students id:int:pk name:str:notnull marks:int
INSERT students id=1 name=Vansh marks=95
              
SELECT students
SELECT students WHERE marks > 80
              
UPDATE students marks=98 WHERE id == 1
DELETE students WHERE marks < 40
              
TABLES
INFO students
COUNT students
COUNT students WHERE marks > 80
              
DROP students
TRUNCATE students

EXIT
""")

    # CREATE

    elif parts[0].upper() == "CREATE":

        if len(parts) < 3:
            print("Usage: CREATE table_name col:type:constraints ...")
            continue

        table_name = parts[1]
        columns = parts[2:]

        result = db.create_table(
            table_name,
            columns
        )

        display_result(result)

    # INSERT

    elif parts[0].upper() == "INSERT":

        if len(parts) < 3:
            print("Usage: INSERT table_name col1=value1 col2=value2 ...")
            continue

        table_name = parts[1]
        row = parse_kv_pairs(parts[2:])

        result = db.insert(
            table_name,
            row
        )

        display_result(result)

    # SELECT

    elif parts[0].upper() == "SELECT":

        if len(parts) < 2:
            print("Usage: SELECT table_name [WHERE column operator value]")
            continue

        table_name = parts[1]
        where = parse_where(parts[2:])

        if parts[2:] and where is None:
            continue

        result = db.select(
            table_name,
            where=where
        )

        display_result(result)

    # UPDATE

    elif parts[0].upper() == "UPDATE":

        if "WHERE" not in (token.upper() for token in parts):
            print("Usage: UPDATE table_name col1=value1 ... WHERE column operator value")
            continue

        table_name = parts[1]

        where_index = next(
            i for i, token in enumerate(parts) if token.upper() == "WHERE"
        )

        set_tokens = parts[2:where_index]
        where_tokens = parts[where_index:]

        values = parse_kv_pairs(set_tokens)
        where = parse_where(where_tokens)

        if where is None:
            continue

        result = db.update(
            table_name,
            values,
            where=where
        )

        display_result(result)

    # DELETE

    elif parts[0].upper() == "DELETE":

        if len(parts) < 2:
            print("Usage: DELETE table_name [WHERE column operator value]")
            continue

        table_name = parts[1]
        where = parse_where(parts[2:])

        if parts[2:] and where is None:
            continue

        result = db.delete(
            table_name,
            where=where
        )

        display_result(result)

    # TABLES

    elif parts[0].upper() == "TABLES":

        for name in db.list_tables():
            print(name)

    # INFO

    elif parts[0].upper() == "INFO":

        if len(parts) < 2:
            print("Usage: INFO table_name")
            continue

        result = db.table_info(parts[1])
        display_result(result)

    # COUNT

    elif parts[0].upper() == "COUNT":

        if len(parts) < 2:
            print("Usage: COUNT table_name [WHERE column operator value]")
            continue

        table_name = parts[1]
        where = parse_where(parts[2:])

        if parts[2:] and where is None:
            continue

        result = db.count(table_name, where=where)
        display_result(result)

    # DROP

    elif parts[0].upper() == "DROP":

        if len(parts) < 2:
            print("Usage: DROP table_name")
            continue

        result = db.drop_table(parts[1])
        display_result(result)

    # TRUNCAT

    elif parts[0].upper() == "TRUNCATE":

        if len(parts) < 2:
            print("Usage: TRUNCATE table_name")
            continue

        result = db.truncate(parts[1])
        display_result(result)

    else:
        print("Unknown command. Type HELP to see available commands.")
