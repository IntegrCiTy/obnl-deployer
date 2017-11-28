import sys
import logging

from coside.communication import RabbitMQCommunicator
from coside.management import Manager

if __name__ == "__main__":
    RabbitMQCommunicator.activate_console_logging(logging.DEBUG)
    c = RabbitMQCommunicator(sys.argv[1], "backend_vhost", "tool", sys.argv[2], "coside/connection.json")

    # d = DockerDeployer()

    manager = Manager(c, None)  # FIXME create a real deployer
    c.manager = manager

    manager.start()


