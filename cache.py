import itertools
from collections import deque
from pathlib import Path
import logging

from file_utils import FileUtils, FileTooBigException


class Cache:
    def __init__(self, capacity):
        self.capacity = capacity  # in bytes
        self.used_space = 0  # in bytes
        self.storage = dict()  # { file_hash: file_content}
        self.usage_queue = deque()

    def get_file_content(self, file_path: str):
        """
        Args:
            file_path: path of a file

        Returns: content of the file at the specified path

        """
        file_path = Path(file_path)  # Path will make it work on all Operating systems
        if not FileUtils.check_if_file_exist(file_path):
            # File doesn't exist
            logging.warning(f'{file_path} doesn\'t exist - action cancelled')
            return

        file_md5_hash = FileUtils.get_file_md5_hash(file_path)
        if file_md5_hash in self.storage:
            self.update_usage_queue(file_md5_hash)
            return self.storage[file_md5_hash]

        else:
            try:
                self.insert_file_to_cache(file_path)
                return self.storage[file_md5_hash]
            except FileTooBigException as e:
                logging.warning(e.args[0])

    def update_usage_queue(self, md5_hash):
        """
        updates a file in usage queue to be the last used file
        Args:
            md5_hash: file md5 hash
        """
        if md5_hash in self.usage_queue:
            self.remove_from_usage_queue(md5_hash)
        self.usage_queue.append(md5_hash)

    def remove_from_usage_queue(self, md5_hash):
        """
        removes a file hash from the usage queue
        Args:
            md5_hash: file md5 hash

        """
        self.usage_queue.remove(md5_hash)

    def get_free_space_size(self):
        """
        Returns: The amount of free space

        """
        return self.capacity - self.used_space

    def is_there_enough_free_space_for_file(self, file_size: int) -> bool:
        """
        Checks if there's enough free space for a file
        Args:
            file_size:

        Returns:
            Boolean
        """
        return self.get_free_space_size() >= file_size

    def remove_file_from_cache(self, md5_hash):
        """
        updates used storage, and removes the file from usage queue and storage
        Args:
            md5_hash: file hash

        """
        self.used_space -= len(self.storage[md5_hash])
        self.storage.pop(md5_hash)
        self.remove_from_usage_queue(md5_hash)

    def check_if_file_exist_in_cache(self, file_path: Path) -> bool:
        """
        Checks if a file exists in cache by using its hash
        Args:
            file_path: path of the desired file

        Returns:
            Whether the file exists in cache

        """
        file_md5_hash = FileUtils.get_file_md5_hash(file_path)
        if file_md5_hash in self.storage:
            self.update_usage_queue(file_md5_hash)
            return True
        return False

    def delete_files_to_insert_new_file(self, new_file_size: int):
        """
        Removes either a file or files to make room for a new file
        Args:
            new_file_size: size of the wanted file
        """
        cumulative_files_size = 0
        for current_file_hash in self.usage_queue:
            # Find the least recently used file
            current_file_size = len(self.storage[current_file_hash])
            cumulative_files_size += current_file_size

            # Removes one file
            if current_file_size + self.get_free_space_size() >= new_file_size:
                self.remove_file_from_cache(current_file_hash)

                break

            # Removes multiple files
            elif cumulative_files_size + self.get_free_space_size() >= new_file_size:
                files_to_delete = [  # Get the least recently used files up to this file (including)
                    file for file in itertools.islice(
                        self.usage_queue,
                        self.usage_queue.index(current_file_hash) + 1
                    )
                ]
                for file in files_to_delete:
                    self.remove_file_from_cache(file)
                break

    def _insert_file_to_cache_storage(self, file_path: Path, new_file_size: int):
        """
        inserts a file to storage and updates the usage queue
        Args:
            file_path: path of the desired file
            new_file_size: size of the wanted file to insert

        """
        md5_hash, file_contents = FileUtils.get_file_contents_and_md5_hash(file_path)
        self.storage[md5_hash] = file_contents
        self.used_space += new_file_size
        self.update_usage_queue(md5_hash)

    def insert_file_to_cache(self, file_path: Path):
        """
        Insert a file to the cache storage using the md5 hash to identify it.
        if there's isn't enough free space available on cache, removes either one file or multiple files, depends on
        how much space needed

        Args:
            file_path: path of the desired file

        """
        new_file_size = FileUtils.get_file_size_in_bytes(file_path)

        if new_file_size > self.capacity:
            raise FileTooBigException(f'{file_path} is bigger than cache, action cancelled')

        if not self.check_if_file_exist_in_cache(file_path):
            # File isn't already in cache

            if not self.is_there_enough_free_space_for_file(new_file_size):
                # There's enough free space - insert file
                self.delete_files_to_insert_new_file(new_file_size)

            self._insert_file_to_cache_storage(file_path, new_file_size)


# Logger
logging.basicConfig(
    encoding='utf-8',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(Path(f'logfile.log')),
        logging.StreamHandler()
    ],
    format='%(asctime)s %(message)s'
)
