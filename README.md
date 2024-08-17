# Cloudflare DDNS Updater

This script updates Cloudflare DNS records with your current public IP address. It retrieves the public IP and checks if any A records in Cloudflare need updating.

## Features

- Automatically fetches your public IP address using the ipify API.
- Compares the current public IP with your existing DNS records in Cloudflare.
- Updates the DNS records only if there's a change in the public IP.

## Requirements

- Python 3.11+
- A Cloudflare account with an API token.
- Docker (optional, for running with Docker).

## Environment Variables

Ensure the following environment variables are set:

- `CF_API_TOKEN`: Your Cloudflare API token.
- `CF_ZONE_ID`: The Cloudflare Zone ID where your DNS records are managed.
- `CF_DNS_RECORD_NAMES`: A comma-separated list of DNS record names to update.

## Installation

### Running Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/soft-titus/cloudflare-ddns.git
   cd cloudflare-ddns
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:

   ```bash
   python main.py
   ```

### Running with Docker

1. Build the Docker image:

   ```bash
   docker build -t cloudflare-ddns .
   ```

2. Run the container:

   ```bash
   docker run --env-file .env --name cloudflare-ddns cloudflare-ddns
   ```

### Running with Docker Compose

1. Ensure your `.env` file is set up with the required environment variables.

2. Run the service with Docker Compose:

   ```bash
   docker compose up
   ```

## Usage

The script will automatically:

1. Retrieve your current public IP.
2. Log in to Cloudflare using the provided API token.
3. Fetch your DNS records and check if the public IP has changed.
4. Update the DNS records if necessary.

## Example `.env` File

```plaintext
CF_API_TOKEN=your_cloudflare_api_token
CF_ZONE_ID=your_cloudflare_zone_id
CF_DNS_RECORD_NAMES=example.com,subdomain.example.com
```

## Contributing

Feel free to submit issues or pull requests if you have any suggestions or improvements.

