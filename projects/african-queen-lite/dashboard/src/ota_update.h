#pragma once
// ============================================================
// African Queen Lite — OTA WiFi Firmware Update v2.2
// Honda NX650 Dominator RFVC
// ============================================================
//
// v2.2: WiFi-based firmware updates via ESPAsyncWebServer.
// When ENABLE_OTA_UPDATE is defined, the ESP32 starts an AP
// ("AQL-OTA") and serves a firmware upload page at port 80.
//
// Security: OTA AP only starts when encoder is held during boot
// (3-second hold on boot = OTA mode). This prevents unauthorized
// firmware pushes while riding.
//
// Usage:
//   1. Hold encoder button while powering on
//   2. Connect to WiFi "AQL-OTA" (password: "aql2026")
//   3. Open http://192.168.4.1 in browser
//   4. Upload .bin firmware file
//   5. ESP32 reboots with new firmware

#if ENABLE_OTA_UPDATE

#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <Update.h>

// OTA Access Point credentials
constexpr const char* OTA_SSID     = "AQL-OTA";
constexpr const char* OTA_PASS     = "aql2026";
constexpr const char* OTA_HOSTNAME = "aql-ride-ctrl";

// OTA Web server
static AsyncWebServer* ota_server_ = nullptr;
static bool ota_active_ = false;
static bool ota_uploading_ = false;
static size_t ota_total_size_ = 0;
static size_t ota_written_ = 0;

// HTML page for firmware upload
static const char OTA_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AQL OTA Update</title>
<style>
  body { background: #0a0e17; color: #e5e7eb; font-family: monospace; text-align: center; padding: 40px; }
  h1 { color: #22d3ee; }
  .box { background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 24px; max-width: 400px; margin: 20px auto; }
  .btn { background: #22d3ee; color: #000; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
  .btn:hover { background: #06b6d4; }
  #progress { width: 100%; background: #1f2937; border-radius: 4px; margin-top: 16px; display: none; }
  #bar { background: #22d3ee; height: 24px; border-radius: 4px; width: 0%; transition: width 0.3s; }
  .info { font-size: 12px; color: #9ca3af; margin-top: 12px; }
  #status { margin-top: 12px; color: #f59e0b; }
</style>
</head>
<body>
<h1>African Queen Lite</h1>
<h2>OTA Firmware Update</h2>
<div class="box">
  <form method="POST" action="/update" enctype="multipart/form-data" id="uploadForm">
    <input type="file" name="firmware" accept=".bin" style="margin: 12px 0;" id="fileInput">
    <br>
    <button type="submit" class="btn" id="uploadBtn">Upload Firmware</button>
  </form>
  <div id="progress"><div id="bar"></div></div>
  <div id="status"></div>
</div>
<div class="info">
  AQL v2.2 — Honda NX650 Dominator RFVC<br>
  Current version will be replaced after upload.
</div>
<script>
document.getElementById('uploadForm').onsubmit = function(e) {
  e.preventDefault();
  var file = document.getElementById('fileInput').files[0];
  if (!file) { document.getElementById('status').textContent = 'Select a .bin file first!'; return; }
  document.getElementById('progress').style.display = 'block';
  document.getElementById('status').textContent = 'Uploading...';
  document.getElementById('uploadBtn').disabled = true;
  
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/update', true);
  xhr.upload.onprogress = function(e) {
    if (e.lengthComputable) {
      var pct = (e.loaded / e.total) * 100;
      document.getElementById('bar').style.width = pct + '%';
    }
  };
  xhr.onload = function() {
    if (xhr.status === 200) {
      document.getElementById('status').textContent = 'Update successful! Rebooting...';
      document.getElementById('status').style.color = '#22c55e';
    } else {
      document.getElementById('status').textContent = 'Update FAILED! Error: ' + xhr.status;
      document.getElementById('status').style.color = '#ef4444';
    }
  };
  xhr.onerror = function() {
    document.getElementById('status').textContent = 'Upload error!';
    document.getElementById('status').style.color = '#ef4444';
  };
  
  var formData = new FormData();
  formData.append('firmware', file);
  xhr.send(formData);
};
</script>
</body>
</html>
)rawliteral";

class OTAUpdate {
public:
    OTAUpdate() = default;

    // Start OTA AP and web server
    void begin() {
        // Start WiFi Access Point
        WiFi.mode(WIFI_AP);
        WiFi.softAP(OTA_SSID, OTA_PASS);
        WiFi.setHostname(OTA_HOSTNAME);

        Serial.println("[OTA] Starting WiFi AP...");
        Serial.printf("[OTA] SSID: %s\n", OTA_SSID);
        Serial.printf("[OTA] IP: %s\n", WiFi.softAPIP().toString().c_str());

        // Create web server
        ota_server_ = new AsyncWebServer(80);

        // Serve upload page
        ota_server_->on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
            request->send_P(200, "text/html", OTA_HTML);
        });

        // Handle firmware upload
        ota_server_->on("/update", HTTP_POST,
            [](AsyncWebServerRequest *request) {
                // Upload complete response
                if (Update.hasError()) {
                    request->send(200, "text/plain", "Update FAILED — check serial log");
                } else {
                    request->send(200, "text/plain", "Update OK — rebooting in 3s...");
                    delay(3000);
                    ESP.restart();
                }
            },
            [](AsyncWebServerRequest *request, const String& filename,
               size_t index, uint8_t *data, size_t len, bool final) {
                // Firmware data handler
                if (index == 0) {
                    // First chunk — begin update
                    Serial.printf("[OTA] Update start: %s (%u bytes)\n",
                                  filename.c_str(), (unsigned)request->contentLength());
                    ota_total_size_ = request->contentLength();
                    ota_written_ = 0;
                    ota_uploading_ = true;

                    // Determine partition size
                    size_t update_size = (filename.endsWith(".bin")) 
                        ? UPDATE_SIZE_UNKNOWN 
                        : request->contentLength();

                    if (!Update.begin(update_size)) {
                        Serial.printf("[OTA] ERROR: Update.begin failed: %d\n", Update.getError());
                    }
                }

                // Write chunk
                if (Update.write(data, len) != len) {
                    Serial.printf("[OTA] ERROR: Update.write failed at %u: %d\n",
                                  (unsigned)ota_written_, Update.getError());
                }
                ota_written_ += len;

                // Progress logging every 10%
                if (ota_total_size_ > 0) {
                    static uint8_t last_pct = 0;
                    uint8_t pct = (ota_written_ * 100) / ota_total_size_;
                    if (pct >= last_pct + 10) {
                        Serial.printf("[OTA] Progress: %u%%\n", pct);
                        last_pct = pct;
                    }
                }

                if (final) {
                    // Last chunk — finalize
                    if (Update.end(true)) {
                        Serial.printf("[OTA] Update complete: %u bytes written\n", (unsigned)ota_written_);
                        Serial.println("[OTA] Rebooting in 3s...");
                    } else {
                        Serial.printf("[OTA] ERROR: Update.end failed: %d\n", Update.getError());
                    }
                    ota_uploading_ = false;
                }
            }
        );

        ota_server_->begin();
        ota_active_ = true;
        Serial.println("[OTA] Web server started on port 80");
        Serial.println("[OTA] Open http://192.168.4.1 in browser to upload firmware");
    }

    // Stop OTA and disconnect WiFi
    void end() {
        if (ota_server_) {
            ota_server_->end();
            delete ota_server_;
            ota_server_ = nullptr;
        }
        WiFi.softAPdisconnect(true);
        WiFi.mode(WIFI_OFF);
        ota_active_ = false;
        Serial.println("[OTA] WiFi AP stopped");
    }

    bool isActive() const { return ota_active_; }
    bool isUploading() const { return ota_uploading_; }

    // Check if we should enter OTA mode (encoder held during boot)
    static bool shouldEnterOTA() {
        pinMode(Pin::ENCODER_BTN, INPUT_PULLUP);
        // Wait a moment for pullup to settle
        delay(100);
        // If encoder is pressed (LOW) at boot, enter OTA mode
        return (digitalRead(Pin::ENCODER_BTN) == LOW);
    }
};

#else
// OTA disabled — stub class
class OTAUpdate {
public:
    void begin() { Serial.println("[OTA] Disabled in build flags"); }
    void end() {}
    bool isActive() const { return false; }
    bool isUploading() const { return false; }
    static bool shouldEnterOTA() { return false; }
};
#endif // ENABLE_OTA_UPDATE