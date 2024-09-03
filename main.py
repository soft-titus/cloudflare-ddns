"""
This script updates Cloudflare DNS records with the current public IP address.
It retrieves the public IP and checks if any A records in Cloudflare need updating.
"""

import logging
import os
import requests
from cloudflare import Cloudflare


def get_public_ip():
    """
    Fetches the current public IP address.
    Returns:
        str: The public IP address as a string.
    """
    return requests.get("https://checkip.amazonaws.com", timeout=10).text


def main():
    """
    Main function that logs into Cloudflare, retrieves the public IP,
    and updates the DNS records if necessary.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    api_token = os.getenv("CF_API_TOKEN")
    if not api_token:
        logging.error("CF_API_TOKEN environment variable not set")
        raise ValueError("CF_API_TOKEN environment variable not set")

    zone_id = os.getenv("CF_ZONE_ID")
    if not zone_id:
        logging.error("CF_ZONE_ID environment variable not set")
        raise ValueError("CF_ZONE_ID environment variable not set")

    record_names = os.getenv("CF_DNS_RECORD_NAMES")
    if not record_names:
        logging.error("CF_DNS_RECORD_NAMES environment variable not set")
        raise ValueError("CF_DNS_RECORD_NAMES environment variable not set")

    logging.info("Logging in to Cloudflare ...")
    cf = Cloudflare(api_token=api_token)

    logging.info("Getting public IP ...")
    public_ip = get_public_ip()
    logging.info("Public IP: %s", public_ip)

    record_name_list = list(set(record_names.split(",")))

    logging.info("Getting DNS records from Cloudflare ...")
    dns_records = cf.dns.records.list(zone_id=zone_id)

    dns_records_exists = []

    logging.info("Updating DNS records ...")
    for dns_record in dns_records:
        if dns_record.type != "A" or dns_record.name not in record_name_list:
            logging.info("Skipping '%s', type = '%s'", dns_record.name, dns_record.type)
            continue
        dns_records_exists.append(dns_record.name)
        if dns_record.content == public_ip:
            logging.info(
                "Skipping '%s', value already equal to '%s'",
                dns_record.name,
                public_ip,
            )
            continue
        cf.dns.records.update(
            zone_id=zone_id,
            dns_record_id=dns_record.id,
            name=dns_record.name,
            type=dns_record.type,
            content=public_ip,
            ttl=int(dns_record.ttl),
            proxied=dns_record.proxied,
        )
        logging.info("DNS record for '%s' updated to '%s'", dns_record.name, public_ip)

    # Find and log DNS records that do not exist in Cloudflare
    dns_records_not_exists = list(set(record_name_list) - set(dns_records_exists))
    if dns_records_not_exists:
        logging.warning(
            "The following DNS records do not exist in Cloudflare: %s",
            dns_records_not_exists,
        )
    else:
        logging.info("All specified DNS records exist in Cloudflare.")


if __name__ == "__main__":
    main()
