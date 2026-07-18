from core.validator import Validator

class Schema:

    @staticmethod
    def build(columns):

        schema = {}

        primary_key_found = False

        for definition in columns:

            parts = definition.split(":")

            if len(parts) < 2:
                return False, "Invalid column definition."

            column_name = parts[0]
            datatype = parts[1]

            if not Validator.is_supported(datatype):
                return False, f"Unsupported datatype '{datatype}'."

            column_schema = {

                "type": datatype,

                "constraints": {

                    "primary_key": False,
                    "unique": False,
                    "nullable": True,
                    "default": None

                }

            }

            for constraint in parts[2:]:

                constraint = constraint.lower()

                if constraint == "pk":

                    if primary_key_found:
                        return False, "Only one PRIMARY KEY is allowed."

                    primary_key_found = True

                    column_schema["constraints"]["primary_key"] = True
                    column_schema["constraints"]["unique"] = True
                    column_schema["constraints"]["nullable"] = False

                elif constraint == "unique":

                    column_schema["constraints"]["unique"] = True

                elif constraint == "notnull":

                    column_schema["constraints"]["nullable"] = False

                elif constraint.startswith("default="):

                    default_value = constraint.split("=", 1)[1]

                    success, converted = Validator.validate(
                        default_value,
                        datatype
                    )

                    if not success:
                        return False, converted

                    column_schema["constraints"]["default"] = converted

                else:

                    return False, f"Unknown constraint '{constraint}'."

            schema[column_name] = column_schema

        return True, schema