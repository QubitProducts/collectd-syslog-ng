#! /usr/bin/python

import collectd
import socket
import csv
import re
import StringIO

MGMT_SOCK_PATH = "/var/lib/syslog-ng/syslog-ng.ctl"
BUFFER_SIZE = 4096
VERBOSE = False


def configure_callback(conf):
    """
    Module load entrypoint.

    Reads collectd module configuration, and populates global variables
    """
    global MGMT_SOCK_PATH, VERBOSE, BUFFER_SIZE

    for node in conf.children:
        if node.key == "Path":
            MGMT_SOCK_PATH = node.values[0]
        elif node.key == "BufferSize":
            BUFFER_SIZE = int(node.values[0])
        elif node.key == "Verbose":
            VERBOSE = node.values[0].lower() == "true"
        else:
            collectd.warning("syslog-ng plugin: Unknown config key: %s."
                             % node.key)

    log_verbose("Configured with sock=%s" % MGMT_SOCK_PATH)


def read_callback():
    """
    Module run entrypoint.

    Reads, parses and dispatches stats.
    """
    raw_stats = read_stats()
    if raw_stats is None:
        collectd.warning("syslog-ng plugin: failed to read stats")
        return

    stats = parse_stats(raw_stats)

    dispatch_stats(stats)


def read_stats(path=MGMT_SOCK_PATH):
    """
    Requests stats over then given socket, and returns them as a file-like
    object.
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    message = ""
    try:
        sock.connect(path)
        sock.send("STATS\n")
        sock.settimeout(0.5)

        while True:
            buf = sock.recv(BUFFER_SIZE)

            message += buf

            if len(buf) < BUFFER_SIZE:
                break
    except socket.timeout:
        collectd.warning("Socket read timeout")
        raise
    finally:
        sock.close()

    if message:
        log_verbose("Read %s from sock" % len(message))
        return StringIO.StringIO(message)


def parse_stats(raw):
    """
    Parses a file like object containing stats into a list of dicts.
    """
    return list(csv.DictReader(raw, delimiter=";"))


def format_key(row):
    """
    Given a row, return the key name it should represent.
    """
    log_verbose("Row: %s" % row)
    sname = row["SourceName"] or "unknown"
    sname = re.sub("[.]", "-", sname)

    sid = row["SourceId"] or "unknown"
    sid = sid.split("#")[0]

    sinst = row["SourceInstance"] or "unknown"
    sinst = re.sub("[;,#.]", "-", sinst)

    stype = row["Type"]
    if not stype:
        collectd.warning("Row had no type: %s" % row)
        return

    return ".".join((sname, sid, sinst, stype))


def dispatch_stats(stats):
    """
    Converts the stats to collectd.Values and dispatches them
    """
    for row in stats:
        value = collectd.Values(plugin="syslog-ng", type="counter")
        key = format_key(row)
        if not key:
            continue

        value.type_instance = key
        value.values = [int(row["Number"])]

        value.dispatch()


def log_verbose(msg):
    if not VERBOSE:
        return
    collectd.info("elasticsearch plugin [verbose]: %s" % msg)

collectd.register_config(configure_callback)
collectd.register_read(read_callback)
