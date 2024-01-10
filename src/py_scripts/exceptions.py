class InvalidFileTypeException (Exception):
    """Raised when the file type referencedd doesnt match the intended file type"""
    pass
        
class FileExistsException (Exception):
    """Raised when an existing file is found at the same path and process does not allow for an overwrite"""
    pass

class ImageConversionException (Exception):
    """Raised when an image conversion tool from a third-party script fails"""