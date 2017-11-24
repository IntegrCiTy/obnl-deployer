import logging

from coside.communication import RabbitMQCommunicator
from coside.deployement import DockerDeployer
from coside.management import Manager

if __name__ == "__main__":
    RabbitMQCommunicator.activate_console_logging(logging.DEBUG)
    c = RabbitMQCommunicator("localhost", "backend_vhost", "tool", "tool", "coside/connection.json")

    d = DockerDeployer()

    manager = Manager(c, d)
    c.manager = manager

    manager.start()


