import os

DEFAULT_EXTENSION_PREFIX:str = '.'

class File:
    full_path:str
    directory: str
    file_name: str
    ext: str
    exists: bool = False
    stats: os.stat_result
    
    def __init__(self, full_path: str):
        self.full_path = full_path
        self.__parse__()
                
        self.exists = os.path.isfile(full_path)
        if self.exists:
            self.__load__()
    
    def __parse__(self):
        dir_parts: [str] = self.full_path.rsplit('/', 1)
        self.directory = dir_parts[0]
        
        file_parts: [str] = dir_parts[1].split(File.DEFAULT_EXTENSION_PREFIX, 1)
        self.file_name = file_parts[0]
        self.ext = file_parts[1]
        
        
    def __load__(self):
        try:
            if not os.path.isfile(self.full_path):
                raise FileNotFoundError()
            
            self.stats = os.stat(self.full_path)
            
        except Exception as e:
            print("failed to load file, %s" % e)