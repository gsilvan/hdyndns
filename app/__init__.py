import typing

from fastapi import FastAPI, Response
from hcloud import Client
from hcloud.zones import Zone, ZoneRecord, ZoneRRSet

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
    records = [
        ("A", ip),
    ]
    if ipv6:
        records.append(("AAAA", ipv6))
    for record_type, ip in records:
        action = client.zones.set_rrset_records(
            rrset=ZoneRRSet(
                zone=Zone(name=zone),
                name=host,
                type=record_type,
            ),
            records=[
                ZoneRecord(value=ip),
            ],
        )
        action.wait_until_finished()
    return Response(status_code=200)
