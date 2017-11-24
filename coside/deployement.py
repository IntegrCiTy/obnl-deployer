import docker
from coside.management import Deployer


class DockerDeployer(Deployer):
    def __init__(self, host="localhost"):
        super().__init__()
        self._host = host

        self._dockers = {}

    def list_blocks(self, block=None):
        pass

    def start_block(self, block):
        client = docker.from_env()
        client.containers.run(image="integrcity/wrapper", command=["wrappers/obnl/fmu.py", "172.17.0.1"],
                              auto_remove=True,
                              volumes={'/home/basso/Workspaces/python/integrcity/wrapper':
                                           {'bind': '/home/ictuser/work', 'mode': 'rw'}},
                              detach=True)

    def stop_block(self, id):
        pass

    def start_cosim(self):
        pass

    def stop_cosim(self):
        pass
