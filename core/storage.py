import json
import os

class Storage:

    @staticmethod
    def save(filename, tables):

        with open(filename, "w") as file:
            json.dump(tables, file, indent=4)

    @staticmethod
    def load(filename):
        if not os.path.exists(filename):
            return {}

        with open(filename, "r") as file:
            return json.load(file)