"""Python Image Service"""

from enum import Enum
import os
import concurrent.futures
from PIL import Image
import py_scripts

from py_scripts.exceptions import FileExistsException, ImageConversionException, InvalidFileTypeException
from py_scripts.file import DEFAULT_EXTENSION_PREFIX

class ImageFormat (Enum):
    UNNKNOWN = "UNKNOWN"
    JPEG = "JPEG"
    TIFF = "TIFF"
    BMP = "BMP"
    GIF = "GIF"
    ICO = "ICO"
    PNG = "PNG"

class ImageFileExtension (Enum):
    UNKNOWN = "UNKNOWN"
    TIFF = "tiff"
    JPEG = "jpg"
    JPG = "jpg"
    PNG = "png"
    GIF = "gif"
    BMP = "bmp"
    TIF = "tif"
    WEBP = "webp"
    SVG = "svg"
    
DEFAULT_DIR_PATH:str = os.getcwd()
DEFAULT_IMAGE_EXTENSION:ImageFileExtension = ImageFileExtension.jpeg
DEFAULT_IMAGE_FORMAT:ImageFormat = ImageFormat.jpeg
DEFAULT_MAX_WORKERS: int = 4

    
class ImageFile (py_scripts.File):
    ext: ImageFileExtension
    format: ImageFormat
    
    def __init__(self, file_path: str):
        super.__init__(file_path)
        self.format = ImageService.get_format_by_extension(self.ext)
    
class ImageService:
    """Image Manipulation Service"""
    
    @staticmethod
    def get_extension_by_format(format: ImageFormat) -> ImageFileExtension:
        """Get Image File Extension by Image Format

        Args:
            format (ImageFormat): Image Format to retrieve extension by

        Returns:
            ImageFileExtension: Image File Extension associated with the Image Format provided
        """
        ext:ImageFileExtension = ImageFileExtension.unknown
        match format:
            case ImageFormat.jpeg:
                ext = ImageFileExtension.jpeg
            case ImageFormat.tiff:
                ext = ImageFileExtension.tiff
        return ext
   
    @staticmethod
    def set_extension_by_format(src_file:str, format:ImageFormat = DEFAULT_IMAGE_FORMAT):
        """Change image file extension by provided image format

        Args:
            src_file (str): full file path to be changed
            format (ImageFormat, optional): Image Format to assign to file path. Defaults to DEFAULT_IMAGE_FORMAT.

        Returns:
            str: file name with provided image format extension
        """
        target_ext: str = ImageService.get_extension_by_format(format).value
        src_file_name:str = src_file.split(DEFAULT_EXTENSION_PREFIX)[0]
        target_file_name: str = src_file_name+DEFAULT_EXTENSION_PREFIX+target_ext
        
        return target_file_name
        
    @staticmethod
    def get_format_by_extension(ext: ImageFileExtension) -> ImageFormat:
        """Get Image Format by extension provided

        Args:
            ext (ImageFileExtension): Image file extension to be evaluated

        Returns:
            ImageFormat: Image Format returned by the extension provided
        """
        image_format:ImageFormat = ImageFormat.unknown
        match ext:
            case ImageFileExtension.jpeg:
                image_format = ImageFormat.jpeg
            case ImageFileExtension.tiff:
                image_format = ImageFormat.tiff
        return image_format
     
    @staticmethod
    def convert_image(src_path: str, target_format: ImageFormat = DEFAULT_IMAGE_FORMAT, quailty:int=100, overwrite:bool = False
    ) -> bool:  
        """Convert Image from one Image format to another

        Args:
            src_path (str): path of image file to be converted
            target_path (str): target file path on new image file name including extension (ex. `/assets/photo.jpeg`)
            target_format (ImageFormat, optional): Target image format. Defaults to DEFAULT_IMAGE_FORMAT.
            quailty (int, optional): desired quality of target image valid range (1-100). Defaults to 100.
            overwrite (bool, optional): allow overrite of existing target file. Defaults to False.

        Raises:
            FileNotFoundError: Source file does not exist
            FileExistsException: Target File exists but overwrite flag set to false preventing it from being overwritten by the save
            ImageConversionException: Something happened in the third-party script during the image conversion
        """
        converted:bool = False
        try:
            image_file:ImageFile = ImageFile(src_path)
            
            if not image_file.exists:
                raise FileNotFoundError("source file `%s` does not exist." % src_path )
            
            target_path = ImageService.set_extension_by_format(src_path, target_format)
            
            if os.path.isfile(target_path) and not overwrite:
                raise FileExistsException("target file `%s` exists and overwrite flag is set to false." % target_path)
            
            im = Image.open(src_path)
            im.thumbnail(im.size)
            im.save(target_path, target_format.value, quality=quailty)
            
            converted = True
        except Exception as e:
            raise ImageConversionException("ImageService.convert_image() failed, %s" % e)
        
        return converted
    
    @staticmethod
    def convert_images_in_directory(dir_path: str, from_format: ImageFormat | None = None, target_format: ImageFormat = DEFAULT_IMAGE_FORMAT, recursive: bool = True, quality:int = 100, overwrite:bool = False, max_workers:int = 4):
        """Convert Images in Directory from one Image Type to Another

        Args:
            dir_path (str): path of directory to be evaluated
            from_format (ImageFormat | None, optional): Image Format to convert from. Defaults to None.
            target_format (ImageFormat, optional): Image Format to Convert To. Defaults to DEFAULT_IMAGE_FORMAT.
            recursive (bool, optional): Convert images in sub-directories. Defaults to True.
            quality (int, optional): quality of image (1-100). Defaults to 100.
            overwrite (bool, optional): Overwrite existing files with the same name. Defaults to False.
            max_workers (int, optional): Maximum number of paralell worker threads . Defaults to 4.
        """
        
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) #setup thread pool
        
        def convert_files(root: str, files: list[str]):
           for file_name in files: # process files in subdirectory
                    file_path = os.path.join(root, file_name)
                    if from_format is not None and ImageService.get_format_by_extension(file_name):
                        pool.submit(ImageService.convert_image(file_path, target_format, quality, overwrite ))
                        
        def convert_directory(dir_path:str):
           for root, dir, files in os.walk(dir_path):
                if recursive: # if recursive, process subdirectories
                    for dir_name in dir:
                        dir_path = os.path.join(root, dir_name)
                        convert_directory(dir_path)
            
                convert_files(root, files) #convert files in directory
                
        convert_directory(dir_path) # trigger the root directory conversion
        pool.shutdown(wait=True) # clean up pools once its done