#!/usr/bin/env bash
# ==============================================================================
# InstituteHub Host Firewall Setup (Ubuntu Linux UFW)
# Enforces least-privilege incoming port access & brute-force rate limits
# ==============================================================================

set -euo pipefail

echo "======================================================"
echo " InstituteHub Production Firewall Configuration (UFW)"
echo "======================================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "[!] Please run this script with root/sudo privileges."
  exit 1
fi

# Reset existing UFW rules to clean state
echo "[*] Resetting existing UFW rules..."
ufw --force reset

# Set default policies: Deny all incoming, Allow all outgoing, Deny routed
echo "[*] Applying default least-privilege traffic policies..."
ufw default deny incoming
ufw default allow outgoing
ufw default deny routed

# Allow SSH with rate limiting (Mitigates brute-force connection attempts)
echo "[*] Enabling rate-limited SSH (Port 22)..."
ufw limit 22/tcp comment 'SSH Rate Limited'

# Allow Web Traffic (HTTP 80 for ACME / Certbot and HTTPS 443)
echo "[*] Enabling Web Ports (HTTP: 80, HTTPS: 443)..."
ufw allow 80/tcp comment 'Nginx HTTP (ACME challenge & 301)'
ufw allow 443/tcp comment 'Nginx HTTPS Production'

# Enable logging
echo "[*] Enabling medium firewall audit logging..."
ufw logging medium

# Enable UFW firewall
echo "[*] Activating UFW firewall..."
ufw --force enable

echo ""
echo "[+] UFW Configuration Status:"
ufw status verbose
echo "======================================================"
echo " Firewall configuration completed successfully."
echo "======================================================"
