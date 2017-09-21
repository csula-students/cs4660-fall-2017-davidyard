"""Files tests simple file read related operations"""

class SimpleFile(object):
    """SimpleFile tests using file read api to do some simple math"""
    def __init__(self, file_path):
        self.numbers = []
        """
        TODO: reads the file by path and parse content into two
        dimension array (numbers)
        """
        import re
        with open(file_path) as f:
            for line in f:
                string_data = re.split('[ \n]', line)
                del string_data[-1]
                int_data = [int(x) for x in string_data]
                self.numbers.append(int_data)
        
        
    def get_mean(self, line_number):
        """
        get_mean retrieves the mean value of the list by line_number (starts
        with zero)
        """
        mean_array = self.numbers[line_number]
        return sum(mean_array)/float(len(mean_array))

    def get_max(self, line_number):
        """
        get_max retrieves the maximum value of the list by line_number (starts
        with zero)
        """
        max_array = self.numbers[line_number]
        return max(max_array)
        

    def get_min(self, line_number):
        """
        get_min retrieves the minimum value of the list by line_number (starts
        with zero)
        """
        min_array = self.numbers[line_number]
        return min(min_array)

    def get_sum(self, line_number):
        """
        get_sum retrieves the sumation of the list by line_number (starts with
        zero)
        """
        sum_array = self.numbers[line_number]
        return sum(sum_array)