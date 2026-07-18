from datetime import datetime

class Validator:

    SUPPORTED_TYPES = {
        "int",
        "float",
        "str",
        "bool",
        "date"
    }
    @staticmethod
    def validate(value, datatype):
        try:

            if datatype == "int":
                return True, int(value)

            elif datatype == "float":
                return True, float(value)

            elif datatype == "str":
                return True, str(value)

            elif datatype == "bool":

                if isinstance(value, bool):
                    return True, value

                value = str(value).lower()

                if value == "true":
                    return True, True

                if value == "false":
                    return True, False

                return False, "Expected True or False."

            elif datatype == "date":

                datetime.strptime(value, "%d-%m-%Y")
                return True, value

            return False, f"Unsupported datatype '{datatype}'."

        except Exception:
            return False, f"Expected datatype '{datatype}'."

    @staticmethod
    def is_supported(datatype):

        return datatype in Validator.SUPPORTED_TYPES