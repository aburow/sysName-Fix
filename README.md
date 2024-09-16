This app has been written to deal with issues that turn up mainly in some security cameras and rPDU's that I have.

In some units the config does appear to be written into flash but us not read back after reboot. Other devices never write the SNMP settings back into flash.

In order to prevent causing longer term flash issues this program reads the current snmp sysName.0 and checks it against the name in sysname_fix.conf.

If the value is set, not further action is taken. If the device has been rebooted and sysName.0 has been cleared or reverted back to the firmware override then an SNMP Set is triggered.

Why?

I've maintained host files, etc for monitoring, etc... doesn't always work. This is a way to force the issue.

Does it work on all devices? Probably not - YMMV.

You need to use the private community. I haven't got a need for SNMPv3 at this stage so this will work on SNMPv1 & SNMPv2c
