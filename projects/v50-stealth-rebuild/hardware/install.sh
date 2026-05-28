#!/bin/bash
# V50 CAN-Bus Setup Script — Run once on first Pi boot
# =====================================================
# Configures Raspberry Pi for V50 CAN dashboard:
# - Enables SPI (for PiCAN2)  
# - Configures SocketCAN interfaces
# - Installs Python dependencies
# - Sets up systemd services
# - Configures framebuffer for 7" TFT
#
# Usage: sudo bash install.sh
set -e

echo "============================================="
echo " Volvo V50 CAN-Bus Dashboard Setup"
echo "============================================="
echo ""

# --- 1. System packages ---
echo "[1/7] Installing system packages..."
apt-get update -qq
apt-get install -y -qq python3-pip python3-pyqt5 can-utils \
    sqlite3 libgpiod2 python3-libgpiod i2c-tools

# --- 2. Python packages ---
echo "[2/7] Installing Python packages..."
pip3 install python-can python-can[socketcan] --break-system-packages 2>/dev/null || \
pip3 install python-can python-can[socketcan]

# --- 3. Enable SPI and I2C ---
echo "[3/7] Enabling SPI and I2C..."
raspi-config nonint do_spi 0 2>/dev/null || true
raspi-config nonint do_i2c 0 2>/dev/null || true

# --- 4. PiCAN2 Duo overlay ---
echo "[4/7] Configuring PiCAN2 Duo HAT..."
# Add MCP2515 CAN controller overlay to /boot/firmware/config.txt
CONFIG_FILE="/boot/firmware/config.txt"
[ -f "$CONFIG_FILE" ] || CONFIG_FILE="/boot/config.txt"

if ! grep -q "mcp2515" "$CONFIG_FILE" 2>/dev/null; then
    cat >> "$CONFIG_FILE" << 'EOF'

# PiCAN2 Duo HAT — MCP2515 CAN controllers
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=mcp2515-can1,oscillator=16000000,interrupt=24
EOF
    echo "  Added PiCAN2 overlay to $CONFIG_FILE"
else
    echo "  PiCAN2 overlay already configured"
fi

# --- 5. CAN interface startup script ---
echo "[5/7] Creating CAN interface startup script..."
cat > /usr/local/bin/v50-can-setup.sh << 'SCRIPT'
#!/bin/bash
# Bring up SocketCAN interfaces for PiCAN2 Duo
set -e

# High-speed CAN (500kbps) — OBD2 port
ip link set can0 type can bitrate 500000 restart-ms 100
ip link set can0 up
echo "can0 up (500kbps)"

# Low-speed CAN (125kbps) — CEM gateway
ip link set can1 type can bitrate 125000 restart-ms 100
ip link set can1 up
echo "can1 up (125kbps)"

# Verify
ip -details link show can0 | head -3
ip -details link show can1 | head -3
SCRIPT
chmod +x /usr/local/bin/v50-can-setup.sh

# --- 6. Systemd services ---
echo "[6/7] Installing systemd services..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy service files
for svc in v50-power-monitor v50-canbus v50-dashboard; do
    if [ -f "$SCRIPT_DIR/${svc}.service" ]; then
        cp "$SCRIPT_DIR/${svc}.service" /etc/systemd/system/
        echo "  Installed $svc.service"
    else
        echo "  WARNING: $svc.service not found"
    fi
done

# Create CAN interface service
cat > /etc/systemd/system/v50-can-interface.service << 'EOF'
[Unit]
Description=Bring up SocketCAN interfaces for PiCAN2 Duo
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/v50-can-setup.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

# Enable services
systemctl daemon-reload
systemctl enable v50-can-interface
systemctl enable v50-power-monitor
systemctl enable v50-canbus
systemctl enable v50-dashboard

# --- 7. Install V50 project ---
echo "[7/7] Setting up V50 project directory..."
V50_DIR="/opt/v50"
mkdir -p "$V50_DIR/canbus" "$V50_DIR/dashboard" "$V50_DIR/logs"

# Copy Python files if running from project directory
PROJECT_DIR="/opt/data/home/vehicle-database/projects/v50-stealth-rebuild"
if [ -d "$PROJECT_DIR" ]; then
    cp "$PROJECT_DIR/canbus/"*.py "$V50_DIR/canbus/"
    cp "$PROJECT_DIR/dashboard/"*.py "$V50_DIR/dashboard/"
    cp "$PROJECT_DIR/hardware/maintenance.json" "$V50_DIR/"
    echo "  Copied V50 Python files to $V50_DIR"
fi

# Create log directory
mkdir -p /var/log/v50
chown pi:pi /var/log/v50

echo ""
echo "============================================="
echo " Setup Complete!"
echo "============================================="
echo ""
echo " Next steps:"
echo "   1. Reboot: sudo reboot"
echo "   2. Verify CAN: ip -details link show can0"
echo "   3. Test CAN:  candump can0 -td A (Ctrl+C to stop)"
echo "   4. Start dashboard: sudo systemctl start v50-dashboard"
echo "   5. Check logs: journalctl -u v50-canbus -f"
echo ""
echo " To uninstall:"
echo "   sudo systemctl disable v50-dashboard v50-canbus v50-power-monitor v50-can-interface"
echo "   sudo rm /etc/systemd/system/v50-*.service"
echo ""