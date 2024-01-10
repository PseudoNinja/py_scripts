import os
import pytest

"""py_scirpts Image Module Test File"""

from py_scripts.image import ImageService

test_dir:str = "src/py_scripts/tests/assets"
test_tiff_image_file_path:str = test_dir+"/test_file.tiff"
test_jpeg_image_file_path:str = test_dir+"/test_file.jpg"

class TestImageService:

    def __cleanup__(self):
        """Deletes generated files from individual tests to prevent unintented files"""
        os.remove(test_jpeg_image_file_path)

    def test_image_service_convert_tiff_to_jpeg_success(self):
        was_converted:bool = ImageService.convert_tiff_to_jpeg(test_tiff_image_file_path)    
        assert was_converted # confirm the file conversion process completed
        assert os.path.isfile(test_jpeg_image_file_path) # confirm output file exists
        self.__cleanup__()
        
    def test_image_service_convert_directory_tiff_to_jpeg_success(self):
        ImageService.convert_directory_tiff_to_jpeg(test_dir)
        assert os.path.isfile(test_jpeg_image_file_path) # confirm output file exists
        self.__cleanup__()
    
    