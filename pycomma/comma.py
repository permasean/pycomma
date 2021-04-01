import json
import typing

class Comma:
    def __init__(
        self, 
        filepath, 
        includes_header=True, 
        delimiter=",", 
        console_mode=False,
    ):
        self.__filepath = filepath

        if isinstance(includes_header, bool):
            self.__includes_header = includes_header
        else:
            raise ValueError("Wrong argument type for includes_header")

        self.__delimiter = delimiter

        if isinstance(console_mode, bool):
            self.__console_mode = console_mode
        else: 
            raise ValueError("Wrong argument type for console_mode")

        try:
            csv_file = open(self.__filepath, mode="r", encoding="utf-8")
            self.__csv_file = csv_file
        except:
            raise IOError("File path is invalid")

        self.__data = []
        self.__header = []
        self.__prepared = False
        self.__json = []

    def _extract_header_from_file(self) -> list:
        header_line = self.__csv_file.readline()
        header = header_line.split(self.__delimiter)
        header[-1] = header[-1].replace("\n", "")
        return header

    def _extract_data_from_file(self) -> list:
        data = []
        line = self.__csv_file.readline()

        while line:
            line = line.split(self.__delimiter)
            line[-1] = line[-1].replace("\n", "")
            data.append(line)
            line = self.__csv_file.readline()

        return data

    def prepare(self):
        if not self.__prepared:
            if self.__includes_header:
                self.__header = self._extract_header_from_file()
            else:
                if len(self.__header) == 0 or self.__header is None:
                    msg = "No header detected. "
                    msg += "Please manually set a header before prepare call."
                    self.__csv_file.close()
                    raise Exception(msg)

            self.__data = self._extract_data_from_file()

            self.__csv_file.close()
            self.__prepared = True
            print("Preparation complete")
        else:
            self.__csv_file.close()
            raise Exception("Redundant preparation call detected")

    def get_header(self) -> list:
        return self.__header

    def set_header(self, header):
        if self.__includes_header:
            msg = "Manual header configuration is disabled. "
            msg += "To enable, use includes_header=False in constructor."
            raise Exception(msg)
        else:
            if not isinstance(header, list):
                msg = "Incorrect format detected for header. "
                msg += "Please configure as a list of strings."
                raise Exception(msg)

            self.__header = header

    def _get_prepared(self) -> bool:
        return self.__prepared

    def _get_includes_header(self) -> bool:
        return self.__includes_header

    def get_data(self) -> list:
        return self.__data

    def to_json(self) -> dict:
        json = {"headers": self.__header, "data": []}
        for row in self.__data:
            json_obj = {}

            for i, h in enumerate(self.__header):
                json_obj[h] = row[i]

            json["data"].append(json_obj)
            
        self.__json = json
        return json

    def show_file_dimensions(self) -> dict:
        return {"columns": len(self.__header), "rows": len(self.__data)}

    def save_as_csv(self, file_path=None):
        return None

    def save_as_json(self, file_path=None):
        if len(self.__json) == 0 or self.__json is None:
            self.to_json()
        
        if file_path is None:
            file_path = "data.json"

        with open(file_path, "w") as json_file:
            json.dump(self.__json, json_file)

        print("Successfully exported as " + file_path)
    
    def file_is_closed(self):
        return self.__csv_file.closed

    def close_file(self):
        if not self.file_is_closed():
            self.__csv_file.close()

    #todo: batch operations, undo + redo operations with version mapping for shell scripting
    #examples: append to certain column, delete substr of certain column, math operations within column or between columns

    
if __name__ == "__main__":
    filepath = "stroke_data.csv"
    comma = Comma(filepath)
    comma.prepare()
    comma.save_as_json()