class Communicator(object):

    def __init__(self):
        super()
        self._manager = None

    @property
    def manager(self):
        return self._manager

    @manager.setter
    def manager(self, manager):
        if manager.communication is self:
            self._manager = manager
        else:
            raise AttributeError("The given manager is not managing this Communicator")

    def start(self):
        """
        Starts the exchange
        :return:
        """
        raise NotImplementedError("Abstract function call.")

    def send_block(self, block, id_block):
        """

        :param block: The block type
        :type block: str
        :param id_block: the id of the block in the db
        :type id_block: str
        :return:
        """
        raise NotImplementedError("Abstract function call.")

    def is_any(self, block):
        """
        Verifies if a block can be simulated by a simulator.

        :param block: the block that has to receive the message
        :type block: str
        :return: `True` if a simulator is listening, otherwise `False`
        """
        raise NotImplementedError("Abstract function call.")

    def is_cosim(self):
        """
        Verify if the co-simulation orchestrator is started.
        """
        raise NotImplementedError("Abstract function call.")

    def launch_cosim(self, init, schedule):
        """
        Launches the co-simulation with the given data.

        :param init:
        :param schedule:
        :return:
        """
        raise NotImplementedError("Abstract function call.")


class Deployer(object):

    def __init__(self):
        super()

    def start_block(self, block, inputs, outputs):
        """

        :param block: the block(s) the simulator shall run
        :type block: str
        :return: the ID of the simulator
        """
        raise NotImplementedError("Abstract function call.")

    def stop_block(self, id):
        """

        :param id: the id of the simulator
        :type id: str
        :return:
        """
        raise NotImplementedError("Abstract function call.")

    def list_blocks(self, block=None):
        """
        Lists all the simulator ids of the given block.
        Must returns all the simulators if block is `None`

        :param block: the block to returns or `None` for all.
        :type block: str
        :return: a list of simulator ids.
        """
        raise NotImplementedError("Abstract function call.")

    def start_cosim(self):
        raise NotImplementedError("Abstract function call.")

    def stop_cosim(self):
        raise NotImplementedError("Abstract function call.")


class Manager(object):

    def __init__(self, communication, deployement):
        self._communicator = communication
        self._deployer = deployement

        self._simulation_name = None
        self._simulation_init = None
        self._schedule = None

    @property
    def communication(self):
        return self._communicator

    @property
    def deployment(self):
        return self._deployer

    def start(self):
        self._communicator.start()

    def initialisation(self, simulation_init):
        self._simulation_init = simulation_init

        for node in self._simulation_init["nodes"]:
            if "block" in node:
                if not self._communicator.is_any(node["block"]):
                    if not self._deployer.list_blocks(node["block"]):
                        inputs = node["inputs"] if "inputs" in node else []
                        outputs =  node["outputs"] if "outputs" in node else []
                        self._deployer.start_block(node["block"], inputs, outputs)
                self._communicator.send_block(node["block"], node["name"])
            else:
                raise AttributeError("The Block of the Node is not set.")

    def schedule(self, schedule):
        self._simulation_name = schedule["simulation_name"]
        self._schedule = schedule

    def start_simulation(self):
        if not self._communicator.is_cosim():
            self._deployer.start_cosim()
        self._communicator.launch_cosim(self._simulation_init, self._schedule)

