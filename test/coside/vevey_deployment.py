import docker
import warnings
from coside.management import Deployer


class VeveyDockerDeployer(Deployer):
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

        if block == "PROFILE":
            client.containers.run(image="gbasso/integrcity-wrapper:vevey",
                                  command=["profile.py",
                                           str_inputs, str_outputs,
                                           "data/profile/backend.json", "data/profile/obnl.json",
                                           name],
                                  auto_remove=True,
                                  detach=True)
        elif block == "STORAGE":
            client.containers.run(image="gbasso/integrcity-wrapper:vevey",
                                  command=["storage.py",
                                           str_inputs, str_outputs,
                                           "data/storage/backend.json", "data/storage/obnl.json",
                                           name],
                                  auto_remove=True,
                                  detach=True)
        elif block == "HEAT_PUMP":
            client.containers.run(image="gbasso/integrcity-wrapper:vevey",
                                  command=["heatpump.py",
                                           str_inputs, str_outputs,
                                           "data/heatpump/backend.json", "data/hp/obnl.json",
                                           name],
                                  auto_remove=True,
                                  detach=True)
        elif block == "HYSTERESIS":
            client.containers.run(image="gbasso/integrcity-wrapper:vevey",
                                  command=["hysteresis.py",
                                           str_inputs, str_outputs,
                                           "data/hysteresis/backend.json", "data/hysteresis/obnl.json",
                                           name],
                                  auto_remove=True,
                                  detach=True)
        elif block == "EFFICIENCY":
            client.containers.run(image="gbasso/integrcity-wrapper:vevey",
                                  command=["efficiency.py",
                                           str_inputs, str_outputs,
                                           "data/efficiency/backend.json", "data/efficiency/obnl.json",
                                           name],
                                  auto_remove=True,
                                  detach=True)
        elif block == "THERMAL_NETWORK":
            client.containers.run(image="gbasso/integrcity-wrapper:vevey",
                                  command=["thermal_netowrk.py",
                                           str_inputs, str_outputs,
                                           "data/tn/backend.json", "data/tn/obnl.json",
                                           name],
                                  auto_remove=True,
                                  detach=True)
        elif block == "FEED_NETWORK":
            client.containers.run(image="gbasso/integrcity-wrapper:vevey",
                                  command=["feed_network.py",
                                           str_inputs, str_outputs,
                                           "data/fn/backend.json", "data/fn/obnl.json",
                                           name],
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
