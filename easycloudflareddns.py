import requests
import re
from collections import namedtuple


class EasyCloudflareDDNS:
    def __init__(self):
        self.config = {}

        params = read_params_from_file("./cloudflare.config")

        assert "email" in params
        assert "root" in params
        assert "names" in params
        assert "dnskey" in params or "globalkey" in params

        self.config["email"] = params["email"]

        if "dnskey" in params:
            self.config["apikey_value"] = "Bearer " + params["dnskey"]
            self.config["apikey_header"] = "Authorization"
        else:
            self.config["apikey_value"] = params["globalkey"]
            self.config["apikey_header"] = "X-Auth-Key"

        self.config["auth_headers"] = {
            "X-Auth-Email": self.config["email"],
            self.config["apikey_header"]: self.config["apikey_value"],
        }

        self.config["root"] = params["root"]
        self.config["names"] = params["names"].split(",")

        self.ip = get_ip()

    def get_zone_id(self, zone_name):
        zones = self.get_all_zones()
        for zone in zones:
            if zone.name == zone_name:
                print(f"Provided root {zone_name} has ID {zone.zone_id}")
                return zone.zone_id

        raise ValueError(f"No zone found called {zone_name}")

    def get_all_zones(self):
        url = "https://api.cloudflare.com/client/v4/zones/"

        response = requests.request("GET", url, headers=self.config["auth_headers"])

        Zone = namedtuple("Zone", ["name", "zone_id"])

        Zones = [Zone(zone["name"], zone["id"]) for zone in response.json()["result"]]

        for zone in Zones:
            print(f"Found {zone}")

        return Zones

    def list_dns_records(self, zone_id):
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/"

        response = requests.request("GET", url, headers=self.config["auth_headers"])

        DNSRecord = namedtuple("DNS_Record", ["name", "id", "zone_id"])

        DNSRecords = [
            DNSRecord(record["name"], record["id"], record["zone_id"])
            for record in response.json()["result"]
        ]

        for dns_record in DNSRecords:
            print(f"Found {dns_record}")

        return DNSRecords

    def patch_record_with_ip(self, zone_id, id):
        url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{id}"

        payload = {"content": self.ip}

        print(f"Patching {zone_id}/dns_records/{id} with {self.ip}")
        response = requests.patch(
            url, json=payload, headers=self.config["auth_headers"]
        )

        print(f"Patch completed with status {response.status_code}")

        assert response.status_code == 200

    def update_ip(self, regex=False):
        all_dns_records = self.list_dns_records(self.get_zone_id(self.config["root"]))

        if regex:
            pass
        else:
            filtered_dns_records = [
                dns_record
                for dns_record in all_dns_records
                if dns_record.name in self.config["names"]
            ]

        for dns_record in filtered_dns_records:
            self.patch_record_with_ip(dns_record.zone_id, dns_record.id)


def get_ip():
    ip = requests.get("http://ifconfig.me").text.strip()

    assert len(ip.split(".")) == 4

    print(f"IP successfully retrieved as {ip}")
    return ip


def read_params_from_file(file_path):
    params = {}
    with open(file_path, "r") as configFile:
        for line in configFile:
            line = line.strip()
            if not line or line[0] == "#":
                continue
            param = line.split("=", 1)
            if len(param) != 2:
                raise ValueError(f"Invalid configuration file line: {line}")
            params[param[0].lower()] = param[1]
    return params


EasyCloudflareDDNS().update_ip()
# c = EasyCloudflareDDNS()
# c.update_ip()
