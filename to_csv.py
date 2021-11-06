import csv


class ToCsv:
    """
    Class that create, delete, and edit csv files
    """

    def __init__(self, output_file: str):
        """
        initialize the path of the output file
        :param output_file:
        """
        self.output_file = output_file
        self.file_obj = open(self.output_file, 'w')

    def empty_file(self):
        """
        function that empties the self.output_file from old data
        """
        open(self.output_file, "w+").close()

    def add_header(self, header: list):
        """
        add the header row in the self.output_fil
        :param header: the names of the columns in the csv file
        """
        writer = csv.writer(self.file_obj)
        writer.writerow(header)  # insert the header in the first row

    def put_data(self, data: dict):
        """
        Puts the given data into the self.output_file with the columns names as given
        :param data: the data to be put in the csv output file
        """
        writer = csv.writer(self.file_obj)

        rows_to_insert = []
        for key in data.keys():
            rows_to_insert.append(list(data[key].values()))

        writer.writerows(rows_to_insert)

    def end_session(self):
        """
        Close the opened self.output_file
        :return:
        """
        self.file_obj.close()
