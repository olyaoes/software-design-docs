from dal import IFileReader
from strategies import IOutputStrategy

class DataProcessor:
    def __init__(self, reader: IFileReader, strategy: IOutputStrategy):
        self.reader = reader
        self.strategy = strategy

    def process_and_output(self, filepath: str):
        data = self.reader.read_file(filepath)
        self.strategy.output_data(data)