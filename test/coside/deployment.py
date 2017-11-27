import docker
import warnings
from coside.management import Deployer

from ict.protobuf.backend.simulation_pb2 import TEST_A, TEST_B, TEST_C


class TestDockerDeployer(Deployer):
    def __init__(self, host="localhost"):
        super().__init__()
        self._host = host
        self._dockers = {}

        self._cosim_container = None

    def list_blocks(self, block=None):
        pass

    def start_block(self, block):
        client = docker.from_env()

        if block == TEST_A:
            client.containers.run(image="gbasso/integrcity-wrapper:test",
                                  command=['[\"seta\"]', '[\"ta\"]', "wrapper/test_a.json"],
                                  auto_remove=True,
                                  detach=True)
        elif block == TEST_B:
            client.containers.run(image="gbasso/integrcity-wrapper:test",
                                  command=['', '[\"tb\"]', "wrapper/test_b.json"],
                                  auto_remove=True,
                                  detach=True)
        elif block == TEST_C:
            client.containers.run(image="gbasso/integrcity-wrapper:test",
                                  command=['[\"t1\",\"t2\"]', '[\"setc\"]', "wrapper/test_c.json"],
                                  auto_remove=True,
                                  detach=True)
        else:
            warnings.warn("The testing Deployer can manage only TEST blocks.")

    def stop_block(self, id):
        warnings.warn("Cannot stop block.")

    def start_cosim(self):
        if self._cosim_container is None:
            client = docker.from_env()

            self._cosim_container = client.containers.run(image="gbasso/integrcity-obnl:test",
                                                          auto_remove=True,
                                                          detach=True)
        else:
            warnings.warn("Co simulator already started.")

    def stop_cosim(self):
        if self._cosim_container is not None:
            self._cosim_container.stop()
            self._cosim_container = None
        else:
            warnings.warn("Co simulator is not running.")
