import json

from coside.management import Communicator
from ict.connection.node import Node

import google.protobuf.json_format as json_format

from ict.protobuf.core_pb2 import MetaMessage
from ict.protobuf.simulation_pb2 import *
from ict.protobuf.db_pb2 import *


class RabbitMQCommunicator(Node, Communicator):

    def __init__(self, host, vhost,  username, password, config_file="connection.json"):
        """
        :param host: the host of AMQP server
        :param vhost: the virtual host name
        :param username: the username to connect to the server
        :param password: the associated password
        :param config_file: the location of the file to load AMQP topology (queues, exchanges, bindings, etc.)
        """
        Node.__init__(self, host, vhost,  username, password, config_file)
        Communicator.__init__(self)

    def start(self):
        Node.start(self)

    def reply_to(self, reply_to, message):
        """
        Replies to a message.

        :param reply_to: where the answer should be sent.
        :param message: the message (str)
        """
        if reply_to:
            m = MetaMessage()
            m.node_name = self._name

            m.details.Pack(message)

    def on_init_message(self, ch, method, props, body):
        RabbitMQCommunicator.LOGGER.debug("Receive message from intialisation.")
        m = MetaMessage()
        m.ParseFromString(body)

        if m.details.Is(SimulationInit.DESCRIPTOR):
            sim = SimulationInit()
            m.details.Unpack(sim)

            self._manager.initialisation(json.loads(json_format.MessageToJson(sim, preserving_proto_field_name=True)))

        elif m.details.Is(Schedule.DESCRIPTOR):
            sch = Schedule()
            m.details.Unpack(sch)

            self._manager.schedule(json.loads(json_format.MessageToJson(sch, preserving_proto_field_name=True)))

        elif m.details.Is(StartSimulation.DESCRIPTOR):
            sta = StartSimulation()
            m.details.Unpack(sta)

            self._manager.start_simulation()

        self._channel.basic_ack(delivery_tag=method.delivery_tag)

    def send_block(self, block, id_block):
        m = MetaMessage()
        m.node_name = self._name

        dr = DataRequired()
        dr.id = id_block
        dr.block = SimulationBlock.Value(block)

        m.details.Pack(dr)

        self.send('', 'coside.cosim.simu.'+block, m.SerializeToString())

    def is_any(self, block):
        queue = self._channel.queue_declare('coside.cosim.simu.'+block)
        consumer_count = queue.method.consumer_count
        RabbitMQCommunicator.LOGGER.debug("consumer count: "+str(consumer_count)+" for block "+block)
        return not consumer_count == 0

    def is_cosim(self):
        queue = self._channel.queue_declare('coside.cosim.simu')
        consumer_count = queue.method.consumer_count
        RabbitMQCommunicator.LOGGER.debug("consumer count: " + str(consumer_count) + " for cosimulation.")
        return not consumer_count == 0

    def launch_cosim(self, init, schedule):
        meta = MetaMessage()
        meta.node_name = self._name

        simulation_message = SimulationInit()
        json_format.ParseDict(init, simulation_message)

        meta.details.Pack(simulation_message)
        self.send("coside.cosim", "coside.cosim.simu", meta.SerializeToString())

        schedule_message = Schedule()
        json_format.ParseDict(schedule, schedule_message)

        meta.details.Pack(schedule_message)
        self.send("coside.cosim", "coside.cosim.simu", meta.SerializeToString())

        meta.details.Pack(StartSimulation())
        self.send("coside.cosim", "coside.cosim.simu", meta.SerializeToString())
