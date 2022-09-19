import json
import os
import typing


class ResourceManager(object):
    """
    Manage resources in specified directory

    """

    def __init__(self, resource_dir: str) -> None:
        super().__init__()
        self.resource_dir = resource_dir

    def get_resources_dir(self) -> str:
        """
        Get path for resources directory
        """
        return self.resource_dir

    def get_resource(self, path: str) -> str:
        """
        Get path for resource
        :param path: POSIX-like path for resource
        """
        comps = path.lstrip('/').split('/')
        return os.path.join(self.get_resources_dir(), *comps)

    def open_resource(self, path: str, **kwargs) -> typing.IO:
        """
        Open resource for path.
        :param path: POSIX-like path for resource
        """
        return open(self.get_resource(path), **kwargs)

    def read_text(self, path: str, **kwargs) -> str:
        """
        Open resource by path and return text without handler
        :param path: POSIX-like path for resource
        """
        with self.open_resource(path, **kwargs) as f:
            data = f.read()

        return data

    def read_json(self, path: str) -> typing.Dict[str, typing.Any]:
        """
        Open resource by path and return json without handler
        :param path: POSIX-like path for resource
        """
        with self.open_resource(path) as f:
            data = json.load(f)

        return data