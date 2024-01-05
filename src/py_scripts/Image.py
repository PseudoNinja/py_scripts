"""Python Image Scripts"""

import os
from PIL import Image

class ImageService:
    """Image Service
    """
    @staticmethod
    def convert_tiff_to_jpeg(file_path: str) -> bool:
        """Convert Image File from TIFF to JPEG

        Args:
            file_path (str): JPEG file to be converted

        Returns:
            bool: conversion process completed for file
        """
        file_parts = os.path.splitext(file_path)
        file_name = file_parts[0]
        file_ext = file_parts[1].lower()
        
        completed:bool = False
        try:
            if file_ext != ".tiff":
                raise Exception("%s is not a valid tiff file" % file_path)
            
            jpeg_file_path = file_name + ".jpg"
            if os.path.isfile(jpeg_file_path):
                raise Exception("skipping %s, jpg file already exists." % file_path)
            
            try:
                im = Image.open(file_name)
                print ("Generating jpeg for %s" % file_name)
                im.thumbnail(im.size)
                im.save(jpeg_file_path, "JPEG", quality=100)
                
            except Exception as e:
                raise Exception("there was an issue converting the file, %s" % e)
            
            print ("%s converted from Tiff to JPEG." % file_path)
            completed = True
        except Exception as e:
            print ("failed to convert file, %s" % e)
        
        return completed
                        
    
    @staticmethod
    def convert_directory_tiff_to_jpeg(dir_path: str = os.getcwd()):
        """Convert TIFF files in Directory to JPEG

        Args:
            dir_path (str, optional): Directort path to be converted. Defaults to directory run from
        """
        
        for root, files in os.walk(dir_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                ImageService.convert_tiff_to_jpeg(file_path)
                            
                            