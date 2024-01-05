"""Python Image Scripts"""

import os
from PIL import Image

class ImageService:
    """Image Service
    """
    @staticmethod
    def convert_tiff_to_jpeg(src_path: str = os.getcwd()):
        """Convert TIFF Images in path to JPEG

        Args:
            src_path (str, optional): Path to convert images in. Defaults to os.getcwd().
        """
        for root, dirs, files in os.walk(src_path, topdown=False):
            for name in files:
                print(os.path.join(root, name))
                if os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
                    if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                        print("A jpeg file already exists for %s" % name)
                    
                    # If a jpeg is *NOT* present, create one from the tiff.
                    else:
                        outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                        try:
                            im = Image.open(os.path.join(root, name))
                            
                            print ("Generating jpeg for %s" % name)
                            
                            
                            im.thumbnail(im.size)
                            im.save(outfile, "JPEG", quality=100)
                        except Exception as e:
                            print ("there was an issue converting the file, %s" % e)
                            