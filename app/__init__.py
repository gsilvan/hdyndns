import typing

from hcloud import Client
from hcloud.zones import Zone, ZoneRRSet, ZoneRecord
from fastapi import FastAPI
from starlette.responses import Response
from starlette.status import HTTP_200_OK

app = FastAPI()


@app.get("/update")
def update(
    zone: str,
    host: str,
    password: str,
    ip: str,
    ipv6: typing.Optional[str] = None,
):
    client = Client(token=password)
    types = ["A"]
    if ipv6:
        types.append("AAAA")
    for type in types:
        create_rrset = False
        try:
            client.zones.get_rrset(zone=Zone(name=zone), name=host, type=type)
        except Exception as e:
            create_rrset = True
        if create_rrset:
            response = client.zones.create_rrset(
                zone=Zone(name=zone),
                name=host,
                type=type,
                ttl=60,
                records=[ZoneRecord(value=ip if type == "A" else ipv6)],
            )
            response.action.wait_until_finished()
        try:
            client.zones.update_rrset_records(
                rrset=ZoneRRSet(
                    zone=Zone(name=zone),
                    name=host,
                    type=type,
                ),
                records=[
                    ZoneRecord(value=ip),
                ],
            )
        except Exception as e:
            pass
    return Response(status_code=HTTP_200_OK)
