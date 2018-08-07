

class ModelAction(object):

    def __init__(self, name, unit='si'):
        """
        Construct a ModelAction - a model action is a measure

        :param name:
        :param unit: choose between si or ip, default is si
        """
        self._list_data = list()
        self._data = None
        self._unit = unit
        self._name = name
        self._default_list = list()
        self._upper_limit = float('inf')
        self._lower_limit = float('-inf')
        self._min = None
        self._max = None
        self._measure_name = "Default"

    def unit(self):
        """Returns the unit system (si or ip)"""
        return self._unit

    def num_of_value(self):
        return len(self._list_data)

    def set_min(self, min_val):
        if min_val < self._lower_limit:
            print("Warning: The input: " + str(min_val) + " is lower than the minimum: " +
                  str(self._lower_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        self._min = min_val

    def set_max(self, max_val):
        if max_val > self._upper_limit:
            print("Warning: The input: " + str(max_val) + " is greater than the maximum: " +
                  str(self._upper_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        self._max = max_val

    def get_data_string(self):
        if not self._list_data:
            if not self._default_list:
                print("Severe, no default list or data list assigned for parametric study")
                print("Error found in measure: " + self._measure_name + ". Stop processing")
                return ""
            else:
                return "[" + ",".join(str(x) for x in self._default_list) + "]"
        else:
            return "[" + ",".join(str(x) for x in self._list_data) + "]"

    def get_datalist(self):
        return self._list_data

    def get_data(self):
        if self._data is None:
            print("Severe: no data assigned for applying measure: " + self._measure_name)
            print("Error: process stopped")
            return ""
        return "[" + str(self._data) + "]"

    def get_boundary(self):
        if self._min is None:
            print("Severe: algorithm requires user to define the minimum value - "
                  "use set_min() to define a minimum value")
            print("No minimum value found in measure: " + self._measure_name + ". Process stopped")
            return ""

        if self._max is None:
            print("Severe: algorithm requires user to define the maximum value - "
                  "use set_max() to define a maximum value")
            print("No maximum value found in measure: " + self._measure_name + ". Process stopped")
            return ""

        return "[" + str(self._min) + "," + str(self._max) + "]"

#    def num_of_combinations(self):
#        comb = 0
#        for i in range(len(self._list_data)):
#            data_list = self._list_data[i]
#            if(comb == 0):
#                comb = len(data_list)
#            else:
#                comb = comb * len(data_list)
#        return comb

    def set_datalist(self, data_list):
        for data in data_list:
            if data < self._lower_limit:
                print("Warning: The input: " + str(data) + " is lower than the minimum: " +
                      str(self._lower_limit) + " for the measure: " + self._measure_name +
                      ". This might be rejected by the server")
            if data > self._upper_limit:
                print("Warning: The input: " + str(data) + " is greater than the maximum: " +
                      str(self._upper_limit) + " for the measure: " + self._measure_name +
                      ". This might be rejected by the server")
        self._list_data = data_list
        return True

    def set_data(self, data):
        if data < self._lower_limit:
            print("Warning: The input: " + str(data) + " is lower than the minimum: " +
                  str(self._lower_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        if data > self._upper_limit:
            print("Warning: The input: " + str(data) + " is greater than the maximum: " +
                  str(self._upper_limit) + " for the measure: " + self._measure_name +
                  ". This might be rejected by the server")
        self._data = data
        return True

    def get_api_name(self):
        return self._name

    @property
    def measure_name(self):
        return self._measure_name
