import json
import typing
import statistics

class Comma:
    def __init__(
        self, 
        filepath, 
        includes_header=True, 
        delimiter=",", 
        console_mode=False,
        configs={
        },
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

        self.__csv_file = None
        self.__data = []
        self.__header = []
        self.__prepared = False
        self.__json = {}
        self.__history = {}
        self.__primary_column_name = None

    def __repr__(self):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        five_rows = self.__data[:5]
        header_row = str("          ".join(self.__header))
        return header_row

    def get_data(self) -> list:
        return self.__data

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

    def get_primary_column_name(self) -> str:
        return str(self.__primary_column_name)

    def set_primary_column_name(self, column_name):
        if isinstance(column_name, str) and column_name in self.__header:
            self.__primary_column_name = column_name

    def _get_prepared(self) -> bool:
        return self.__prepared

    def _get_console_mode(self) -> bool:
        return self.__console_mode

    def _get_includes_header(self) -> bool:
        return self.__includes_header

    def _manual_load_csv_for_testing(self):
        csv_file = open(self.__filepath, mode="r", encoding="utf-8")
        self.__csv_file = csv_file

    def _manual_close_file_for_testing(self):
        if not self.file_is_closed():
            self.__csv_file.close()

    def dimension(self) -> dict:
        return {"columns": len(self.__header), "rows": len(self.__data)}

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
            csv_file = open(self.__filepath, mode="r", encoding="utf-8")
            self.__csv_file = csv_file

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

    def _to_json(self) -> dict:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        json = {"headers": self.__header, "data": []}
        for row in self.__data:
            json_obj = {}

            for i, h in enumerate(self.__header):
                json_obj[h] = row[i]

            json["data"].append(json_obj)
            
        self.__json = json

    def get_json(self) -> dict:
        self._to_json()
        return self.__json

    def join_with_delimiter(self, a_list, delimiter=",") -> str:
        return str(delimiter.join(a_list))

    def save_as_csv(self, file_path=None, delimiter=","):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        if file_path is None:
            file_path = "data.csv"

        with open(file_path, "w") as csv_file:
            header_string = join_with_delimiter(self.__header, delimiter)
            header_string += "\n"
            csv_file.write(header_string)

            for row in self.__data:
                row_string = join_with_delimiter(row, delimiter)
                row_string += "\n"
                csv_file.write(row_string)

        print("Successfully exported as " + file_path)

    def save_as_json(self, file_path=None):
        if not self.__json or self.__json is None:
            self._to_json()
        
        if file_path is None:
            file_path = "data.json"

        with open(file_path, "w") as json_file:
            json.dump(self.__json, json_file)

        print("Successfully exported as " + file_path)

    def file_is_closed(self) -> bool:
        return self.__csv_file.closed

    def undo(self):
        if not self.__console_mode:
            raise Exception("Must enable console mode to use history features")
        return None

    def redo(self):
        if not self.__console_mode:
            raise Exception("Must enable console mode to use history features")
        return None

    def append(self, column_name, str_to_append):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        try:
            str_to_append = str(str_to_append)
        except ValueError:
            raise ValueError("Argument cannot be converted to String")

        for i in range(len(self.__data)):
            self.__data[i][column_idx] += str_to_append

        if not self.__console_mode:
            return self.__data

    def replace(self, column_name, substr, replace_with):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        try:
            substr = str(substr)
            replace_with = str(replace_with)
        except:
            raise ValueError("Arguments cannot be converted to String")

        for i in range(len(self.__data)):
            if substr.lower() in self.__data[i][column_idx].lower():
                temp = self.__data[i][column_idx].lower()
                self.__data[i][column_idx] = temp.replace(substr, replace_with)

        if not self.__console_mode:
            return self.__data

    def change(
        self, 
        column_name, 
        changing, 
        change_to, 
        case_matters=False
        ):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        try:
            changing = str(changing)
            change_to = str(change_to)
        except:
            raise ValueError("Arguments cannot be converted to String")

        for i in range(len(self.__data)):
            if case_matters:
                if self.__data[i][column_idx] == changing:
                    self.__data[i][column_idx] = change_to
            else:
                if self.__data[i][column_idx].lower() == changing.lower():
                    self.__data[i][column_idx] == change_to

        if not self.__console_mode:
            return self.__data

    def fill_empty(self, column_name, replace_with):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try:
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        try:
            replace_with = str(replace_with)
        except ValueError:
            raise ValueError("Argument cannot be converted to String")

        count = 0
        for i in range(len(self.__data)):
            if not self.__data[i][column_idx]:
                if replace_with:
                    self.__data[i][column_idx] = replace_with
                else:
                    self.__data[i][column_idx] = "None"
                count += 1
        
        print("Fill Count: " + str(count))

    def sum(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        result = 0
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                result += num
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue
                
        return result

    def median(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")
        
        converted_list = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                converted_list.append(num)
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue

        converted_list.sort()
                
        return statistics.median(converted_list)

    def mean(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        column_values = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                column_values.append(num)
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue

        return statistics.mean(column_values)

    def stdev(self, column_name, ignore_na=False) -> float:
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        try: 
            column_idx = self.__header.index(str(column_name))
        except ValueError:
            raise ValueError("Column " + str(column_name) + " does not exist")

        column_values = []
        for i in range(len(self.__data)):
            value = self.__data[i][column_idx]

            try:
                num = float(value)
                column_values.append(num)
            except ValueError:
                if not ignore_na:
                    msg = "Value at row " + str(i)
                    msg += " cannot be converted to Float. "
                    msg += "To ignore, use ignore_na=True"
                    raise ValueError(msg)
                else:
                    continue

        return statistics.stdev(column_values)

    def minimum(self, column_name):
        return None

    def maximum(self, column_name):
        return None

    def value_counts(self, column_name):
        return None

    def add_column(self, column_name, data):
        # data argument should be a list
        return None

    def delete_column(self, column_name):
        return None

    def rearrange_columns(self, header):
        # header should be a list of column names in desired arrangement
        return None

    def switch_columns(self, x_column_name, y_column_name):
        return None

    def unique_values(self, column_name):
        return None

    def column_stat(self, column_name):
        return None

    def find_row_index_by_value(self, primary_column_value):
        if self.__primary_column_name is None:
            raise Exception("No primary column detected. Set a primary column")

        return None

    def find_row_indices_by_value(self, primary_column_values):
        if self.__primary_column_name is None:
            raise Exception("No primary column detected. Set a primary column")

        if isinstance(primary_column_values, list):
            return None
        else:
            raise Exception("Incorrect param type detected. Must be a list")
        return None

    def delete_row_by_index(self, row_idx):
        if self._primary_column_name is None:
            raise Exception("No primary column detected. Set a primary column")

    def delete_rows_by_indices(self, row_indices):
        if self._primary_column_name is None:
            raise Exception("No primary column detected. Set a primary column")

    def add_row(self, row):
        if not isinstance(row, list):
            raise Exception("Incorrect param type detected. Must be a list")

        if len(row) != len(self.__header):
            raise Exception("Length of row must match the number of columns")

        return None

    def show(self):
        if not self.__prepared:
            raise Exception("Must call comma.prepare() first")

        five_rows = self.__data[:5]
        header_row = "          ".join(self.__header)
        print(header_row)

    def show_json(self):
        # prints first 5 rows in json
        return None
    

    #todo: batch operations
    #examples: append to certain column, delete substr of certain column, math operations within column or between columns

if __name__ == "__main__":
    filepath = "stroke_data.csv"
    comma = Comma(filepath)
    comma.prepare()
    comma.save_as_csv()