# I need to rewrite it using classes

import os
from mimetypes import guess_type
from subprocess import check_call

from PIL import Image


def add_path_suffix(path, suffix):
    path_part, dot, extension = path.rpartition('.')
    path_new = dot.join([path_part + f'_{suffix}', extension])
    return path_new


def change_path_extension(path, extension_new):
    return ''.join(path.rpartition('.')[:2] + (extension_new,))


class ImageThumbnailer:
    SAVE_OPTIONS = {}

    @classmethod
    def resize(cls, path_old, path_new, width, can_optimize=True):
        image = Image.open(path_old)
        source_x, source_y = map(float, image.size)
        scale = source_y / source_x
        target_x, target_y = width, int(round(scale * width))

        image_resized = image.resize(
            (target_x, target_y),
            resample=Image.ANTIALIAS
        )
        image_resized.save(path_new, **cls.SAVE_OPTIONS)
        return path_new

    @classmethod
    def convert_to_webp(cls, path_old, path_new, width):
        path_temporary = add_path_suffix(path_old, '_temporary')
        cls.resize(path_old, path_temporary, width)
        image = Image.open(path_temporary)
        image.save(path_new, format='webp', quality=90)
        check_call(['rm', '-rf', path_temporary])
        return path_new


class ImageThumbnailerJPEG(ImageThumbnailer):
    SAVE_OPTIONS = {'quality': 90, 'progressive': True}


class ImageThumbnailerPNG(ImageThumbnailer):
    SAVE_OPTIONS = {'optimize': True}


class ImageThumbnailerGIF(ImageThumbnailer):
    @classmethod
    def resize(cls, path_old, path_new, width, can_optimize=True):
        command = [
            'gifsicle', '--resize-width', f'{width}',
            '--no-extensions', '-i', path_old, '-o', path_new,
        ]
        if can_optimize:
            command.extend(['-O3', '--colors', '96'])
        check_call(command)
        return path_new

    @classmethod
    def convert_to_webp(cls, path_old, path_new, width):
        path_temporary = add_path_suffix(path_old, '_temporary')
        cls.resize(path_old, path_temporary, width, can_optimize=False)

        command = [
            'gif2webp', '-lossy', '-min_size', '-quiet',
            '-metadata', 'none', path_temporary, '-o', path_new
        ]
        check_call(command)
        check_call(['rm', '-rf', path_temporary])
        return path_new


class ImageProcessor:
    MIMETYPE_WEBP = 'image/webp'
    MIMETYPE_JPEG = 'image/jpeg'
    MIMETYPE_PNG = 'image/png'
    MIMETYPE_GIF = 'image/gif'

    MIMETYPE_THUMBNAILERS = {
        MIMETYPE_JPEG: ImageThumbnailerJPEG,
        MIMETYPE_PNG: ImageThumbnailerPNG,
        MIMETYPE_GIF: ImageThumbnailerGIF,
    }

    BREAKPOINTS = [480, 960, 1180, 1400, 1660, 1920, 2240, 2560]

    def __init__(self, image):
        self.image = image
        self.postfix = round(image.modified_at.timestamp())
        self.mimetype = self.get_mimetype(image)
        self.thumbnailer = self.MIMETYPE_THUMBNAILERS[self.mimetype]

    @classmethod
    def get_mimetype(cls, image):
        mimetype = guess_type(image.path)[0]
        if mimetype not in cls.MIMETYPE_THUMBNAILERS:
            raise ValueError(f'Unknown file mimetype {mimetype}')
        return mimetype

    def create_thumbnails(self):
        return self.get_thumbnails(can_create=True)

    def delete_thumbnails(self):
        directory, slash, original_file = self.image.path.rpartition('/')
        files = os.listdir(directory)
        for file in files:
            if (file != original_file) and (f'{self.postfix}' not in file):
                os.remove(directory + slash + file)

    def get_thumbnails(self, can_create=False, can_delete=False):
        structure = {
            'image': [],
            'sources': {self.MIMETYPE_WEBP: []}
        }

        breakpoints = [
            breakpoint for breakpoint in self.BREAKPOINTS
            if breakpoint < self.image.width
        ]
        if len(breakpoints) != len(self.BREAKPOINTS):
            breakpoints.append(self.image.width)

        for breakpoint in breakpoints:
            path = add_path_suffix(self.image.path, f'{self.postfix}_{breakpoint}')
            path_webp = change_path_extension(path, 'webp')

            if can_create:
                self.thumbnailer.resize(self.image.path, path, breakpoint)
                self.thumbnailer.convert_to_webp(self.image.path, path_webp, breakpoint)

            structure['sources'][self.MIMETYPE_WEBP].append(
                {'path': path_webp, 'width': breakpoint}
            )
            structure['image'].append({'path': path, 'width': breakpoint})

        if can_delete:
            self.delete_thumbnails()

        return structure
