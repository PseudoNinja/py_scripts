# py_scripts

## Description

Useful Python scripts and utilities

## Installation instructions

```
python -m pip install "https://github.com/PseudoNinja/py_scripts"
```

## Usage

### Image Service

#### ImageService.convert_tiff_to_jpeg

_Description:_ Convert Image File from TIFF to JPEG

_Args:_

-   file_path (str): TIFF file to be converted

_Returns:_

-   bool: conversion process completed for file

_Example:_

```[python]
was_converted:bool = ImageService.convert_tiff_to_jpeg(test_tiff_image_file_path)
```

#### ImageService.convert_directory_tiff_to_jpeg

_Description:_ Convert TIFF files in Directory to JPEG
_Args:_

-   dir_path (str, optional): Directort path to be converted. Defaults to directory run from

_Example:_

```[python]
ImageService.convert_directory_tiff_to_jpeg(test_dir)
```
