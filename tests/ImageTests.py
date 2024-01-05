"""py_scirpts Image Module Test File"""

from py_scripts.Image import ImageService

test_image_path:str = "/assets"

def test_image_service_convert_tiff_to_jpeg_success():
    ImageService.convert_tiff_to_jpeg(test_image_path)    