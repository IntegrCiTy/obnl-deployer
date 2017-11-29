import docker
import warnings
from coside.management import Deployer


class TestDockerDeployer(Deployer):
    def __init__(self, host="localhost"):
        super().__init__()
        self._host = host
        self._dockers = {}

        self._cosim_container = None

    def list_blocks(self, block=None):
        pass

    def start_block(self, name, block, inputs, outputs):
        client = docker.from_env()

        # Convert str ot be pass to a shell.
        str_inputs = str(inputs).replace("'", '"').replace(" ", "")
        str_outputs = str(outputs).replace("'", '"').replace(" ", "")

        if block == "TEST_A":
            client.containers.run(image="gbasso/integrcity-wrapper:test",
                                  command=[str_inputs, str_outputs, "wrapper/backend.json", "wrapper/obnl.json"],
                                  auto_remove=True,
                                  detach=True)
        elif block == "TEST_B":
            client.containers.run(image="gbasso/integrcity-wrapper:test",
                                  command=[str_inputs, str_outputs, "wrapper/test_b.json", "wrapper/obnl_b.json"],
                                  auto_remove=True,
                                  detach=True)
        elif block == "TEST_C":
            client.containers.run(image="gbasso/integrcity-wrapper:test",
                                  command=[str_inputs, str_outputs, "wrapper/test_c.json", "wrapper/obnl_c.json"],
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
