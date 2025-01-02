import json

import requests
from fastapi import FastAPI
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

app = FastAPI()


class HetznerDNS:
    API_BASE_URL = "https://dns.hetzner.com/api/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def zone_id(self, dns_name: str) -> str:
        response = requests.get(
            url=f"{self.API_BASE_URL}/zones",
            headers={
                "Auth-API-Token": self.api_key,
            },
        )
        zones = response.json().get("zones")
        for zone in zones:
            if zone["name"] == dns_name:
                return zone["id"]
        return ""

    def record_id(self, dns_record: str, zone_id: str) -> str:
        response = requests.get(
            url=f"{self.API_BASE_URL}/records",
            params={
                "zone_id": f"{zone_id}",
            },
            headers={
                "Auth-API-Token": self.api_key,
            },
        )
        records = response.json().get("records")
        for record in records:
            if record["name"] == dns_record:
                return record["id"]
        return ""

    def create_record(
        self,
        name: str,
        ttl: int,
        type: str,
        value: str,
        zone_id: str,
    ) -> str:
        response = requests.post(
            url=f"{self.API_BASE_URL}/records",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": self.api_key,
            },
            data=json.dumps(
                {
                    "name": name,
                    "ttl": ttl,
                    "type": type,
                    "value": value,
                    "zone_id": zone_id,
                }
            ),
        )
        record = response.json().get("record")
        return record.get("id")

    def update_record(
        self, name: str, ttl: int, type: str, value: str, zone_id: str, record_id: str
    ) -> str:
        response = requests.put(
            url=f"{self.API_BASE_URL}/records/{record_id}",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": self.api_key,
            },
            data=json.dumps(
                {
                    "name": name,
                    "ttl": ttl,
                    "type": type,
                    "value": value,
                    "zone_id": zone_id,
                }
            ),
        )
        record = response.json().get("record")
        return record.get("id")


@app.get("/update")
def update(zone: str, host: str, password: str, ip: str):
    dns = HetznerDNS(password)
    _zone_id = dns.zone_id(zone)
    if len(_zone_id) == 0:
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    _record_id = dns.record_id(host, _zone_id)
    if len(_record_id) == 0:
        # Create new record if no record is found
        dns.create_record(host, 60, "A", ip, _zone_id)
    else:
        # Update existing record
        dns.update_record(host, 60, "A", ip, _zone_id, _record_id)
    return Response(status_code=HTTP_200_OK)
