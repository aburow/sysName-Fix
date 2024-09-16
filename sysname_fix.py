import asyncio
import csv
from pysnmp.hlapi.asyncio import *
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

async def snmp_fix(devip, community, sysname):
    snmp_engine = SnmpEngine()

    # Get the current sysName for confirmation
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        snmp_engine,
        CommunityData(community),
        UdpTransportTarget((devip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0))
    )

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    else:
        for varBind in varBinds:
            currentName = varBind[1].prettyPrint()

    # If sysName is not set correctly then set it.
    if sysname != currentName:
        errorIndication, errorStatus, errorIndex, varBinds = await setCmd(
            snmp_engine,
            CommunityData(community),
            UdpTransportTarget((devip, 161)),
            ContextData(),
            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0), sysname)
        )
        if errorIndication:
            print(f"Error: {errorIndication} while setting sysName for {devip}")
        elif errorStatus:
            print(f"Error: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
        else:
            print(f"Successfully set sysName to {sysname} for {devip}")

def read_input_from_csv(file_path):
    devices = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            devices.append({
                'devip': row['devip'].strip(),
                'community': row['community'].strip(),
                'sysname': row['sysname'].strip()
            })
    return devices

async def main():
    devices = read_input_from_csv('sysname_fix.conf')
    tasks = [snmp_fix(device['devip'], device['community'], device['sysname']) for device in devices]
    await asyncio.gather(*tasks)

# main()
asyncio.run(main())
