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
):
    client = Client(token=password)
    records = [
        ("A", ip),
    ]
    for record_type, ip in records:
        client.zones.set_rrset_records(
            rrset=ZoneRRSet(
                zone=Zone(name=zone),
                name=host,
                type=record_type,
            ),
            records=[
                ZoneRecord(value=ip),
            ],
        )
    return Response(status_code=200)
