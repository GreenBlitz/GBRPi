from typing import Callable, Any

from networktables import NetworkTables
from networktables.networktable import NetworkTable


class TableConn:
    """
    a simplified wrapper for a network table connection
    NOTE! the table initializes asynchronously, if you need a value immediately after initializing,
        use time.sleep before getting it

    :param ip: the network table server's ip (usually the RoboRIO's ip)
    :param table_name: the network table's name
    :param initialize: whether or not to initialize the network tables (default is true)
    """
    # NetworkTables notifier kinds.
    NT_NOTIFY_NONE = 0x00
    NT_NOTIFY_IMMEDIATE = 0x01  # initial listener addition
    NT_NOTIFY_LOCAL = 0x02  # changed locally
    NT_NOTIFY_NEW = 0x04  # newly created entry
    NT_NOTIFY_DELETE = 0x08  # deleted
    NT_NOTIFY_UPDATE = 0x10  # value changed
    NT_NOTIFY_FLAGS = 0x20  # flags changed

    @staticmethod
    def __fix_func(func: Callable[[Any], None]):
        return lambda source, key, value, is_new: func(value)

    def __init__(self, ip: str, table_name: str, initialize=True):
        if initialize:
            NetworkTables.initialize(ip)
        self.table: NetworkTable = NetworkTables.getTable(table_name)

    def set_table(self, table: NetworkTable):
        """
        sets the inner network table

        :param table: the inner network table
        """
        self.table = table

    def get(self, key: str, default: Any = None) -> Any:
        """
        retrieve a value from the network table

        :param key: the key of the value
        :param default: the default value to return if the key does not exist
        :return: the value from the network table
        """
        return self.table.getValue(key, default)

    def set(self, key: str, value: Any):
        """
        sets a value in the network table
        :param key:
        :param value:
        """
        self.table.putValue(key, value)

    def add_entry_change_listener(self, func: Callable[[Any], None], key: str, notify_now=True, notify_local=True):
        """
        add a function to be called every time a specific entry is changed on the vision table

        :param func: the callback function, receives the new value of the entry as the only argument
        :param key: the key to track
        :param notify_now: whether or not to call the function with the current value (if exists), default is true
        :param notify_local: whether or not to notify if the change was made locally, default is true
        """
        self.table.addEntryListener(self.__fix_func(func), key=key, localNotify=notify_local,
                                    immediateNotify=notify_now)
