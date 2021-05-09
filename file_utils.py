import os
import hashlib
from pathlib import Path


class FileUtils:
    """
    This class handles file related actions. Has only static methods.
    """

    @staticmethod
    def get_file_size_in_bytes(file_path: Path) -> int:
        """
        Returns the size of the file in bytes
        Args:
            file_path: path of the desired file

        Returns:
            size of file

        """
        return os.stat(file_path).st_size

    @staticmethod
    def get_file_md5_hash(file_path: Path, buffer_size: int = 65536) -> str:
        """
        Gets the MD5 hash
        Args:
            file_path: path of the desired file
            buffer_size: the size of each chunk when reading file, default is 64kb

        Returns:
            The MD5 hash of the desired file

        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            # Read file in chunks
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                md5.update(data)

        return md5.hexdigest()

    @staticmethod
    def get_file_contents_and_md5_hash(file_path: Path, buffer_size: int = 65536) -> tuple[str, bytes]:
        """
        Gets the md5 hash and contents of a file
        Args:
            file_path:  path of a file
            buffer_size: the size of each chunk when reading file, default is 64kb
        Returns:
            a tuple: (md5 hash, file contents)
        """
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            file_content = bytes()

            # Read file in chunks
            while True:
                data = f.read(buffer_size)
                file_content += data
                if not data:
                    break  # End of file
                md5.update(data)

        return md5.hexdigest(), file_content

    @staticmethod
    def get_file_contents(file_path: Path, buffer_size: int = 65536) -> bytes:
        """
        gets the content of a file
        Args:
            file_path: path of a file
            buffer_size: the size of each chunk when reading file, default is 64kb

        Returns:
            Contents of file
        """
        with open(file_path, 'rb') as f:
            file_content = bytes()

            # Read file in chunks
            while True:
                data = f.read(buffer_size)
                file_content += data
                if not data:
                    break  # End of file

        return file_content

    @staticmethod
    def check_if_file_exist( file_path: Path):
        return file_path.is_file()


class FileTooBigException(BaseException):
    pass
