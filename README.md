# syslog-ng collectd plugin

A plugin for [collectd](http://collectd.org/) to gather statistics about a
running [syslog-ng](https://en.wikipedia.org/wiki/Syslog-ng) daemon.

The plugin takes a very systematic approach to collecting stats. The syslog-ng
control socket is asked to provide stats, and these are then parsed into keys
and values. The information gathered can be seen using `syslog-ng-ctl`:

```
username@hostname:~$ sudo syslog-ng-ctl stats
SourceName;SourceId;SourceInstance;State;Type;Number
source;s_414427;;a;processed;0
source;s_src;;a;processed;5067
global;sdata_updates;;a;processed;1918943
center;;received;a;processed;5067
destination;d_daemon;;a;processed;1905573
destination;d_relay;;a;processed;1919108
destination;d_error;;a;processed;477
destination;d_syslog;;a;processed;1911933
dst.syslog;d_local#0;tcp,localhost:601;a;dropped;0
dst.syslog;d_local#0;tcp,localhost:601;a;processed;1919108
dst.syslog;d_local#0;tcp,localhost:601;a;stored;0
destination;d_newscrit;;a;processed;0
global;msg_clones;;a;processed;0
destination;d_mail;;a;processed;7
destination;d_uucp;;a;processed;0
destination;d_kern;;a;processed;377
destination;d_newserr;;a;processed;0
destination;d_xconsole;;a;processed;2227
source;s_local;;a;processed;0
destination;d_lpr;;a;processed;0
center;;queued;a;processed;7675090
destination;d_debug;;a;processed;2
src.internal;s_src#2;;a;processed;5067
src.internal;s_src#2;;a;stamp;1437125675
src.none;;;a;processed;0
src.none;;;a;stamp;0
destination;d_auth;;a;processed;7439
destination;d_user;;a;processed;127
destination;d_local;;a;processed;1919546
global;payload_reallocs;;a;processed;75
destination;d_cron;;a;processed;789
destination;d_console_all;;a;processed;2227
destination;d_newsnotice;;a;processed;0
source;s_286784;;a;processed;0
dst.syslog;d_relay#0;tls,syslog.example.com:514;a;dropped;0
dst.syslog;d_relay#0;tls,syslog.example.com:514;a;processed;1919108
dst.syslog;d_relay#0;tls,syslog.example.com:514;a;stored;0
destination;d_messages;;a;processed;5258
source;s_527240;;a;processed;0
destination;d_console;;a;processed;0
```

In this example, the row `dst.syslog;d_relay#0;tls,syslog.example.com:514;a;processed;1919108`
will be converted into a gauge named `dst-syslog.d_relay.tls-syslog-example-com-514.processed`
with value `1919108`.

## Install

1. Dump `syslog-ng.py` into your collectd python plugin directory (usually
   `/usr/lib/collectd/plugins/python`)
2. Dump `syslog-ng.conf` into your collectd config directory (usually
   `/etc/collectd/conf.d`)
3. Modify configuration as needed (custom syslog-ng control socket path, verbose
   etc)
4. Restart collectd

## Requirements

- Collectd 4.9+
