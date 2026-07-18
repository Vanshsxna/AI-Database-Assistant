from core.validator import Validator

class Constraints:

    @staticmethod
    def validate(table, row):

        schema = table["schema"]
        rows = table["rows"]

        validated_row = {}

        for column, info in schema.items():

            datatype = info["type"]
            constraints = info["constraints"]

            value = row.get(column)

            if value is None or value == "":

                if constraints["default"] is not None:
                    value = constraints["default"]

            if (
                constraints["nullable"] is False
                and
                (value is None or value == "")
            ):
                return (
                    False,
                    f"Column '{column}' cannot be NULL."
                )

            if value is not None:

                success, converted = Validator.validate(
                    value,
                    datatype
                )

                if not success:
                    return (
                        False,
                        f"{column}: {converted}"
                    )

                value = converted

            validated_row[column] = value


        for column, info in schema.items():

            constraints = info["constraints"]

            if (
                constraints["primary_key"]
                or
                constraints["unique"]
            ):

                value = validated_row[column]

                for existing_row in rows:

                    if existing_row[column] == value:

                        return (
                            False,
                            f"Duplicate value '{value}' in column '{column}'."
                        )

        return (
            True,
            validated_row
        )