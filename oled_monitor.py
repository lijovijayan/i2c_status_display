import time
import socket
import psutil
import traceback
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

# Load a smaller monospace font
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", size=12)
except Exception as e:
    print("[WARN] Failed to load monospace font, falling back to default.")
    font = ImageFont.load_default()

# Initialize OLED display
try:
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)
    display_available = True
except Exception as e:
    print("[ERROR] Failed to initialize display:")
    print(traceback.format_exc())
    display_available = False

# Get local network IP (not 127.0.0.1)
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/A"

# Get CPU temperature
def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read()) / 1000.0
    except:
        return 0.0

# Main loop
page = 0

while True:
    try:
        ip = get_ip()
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        temp = get_cpu_temp()
        uptime_sec = time.time() - psutil.boot_time()
        uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_sec))

        if display_available:
            with canvas(device) as draw:
                if page == 0:
                    draw.text((0, 0),   f"IP:   {ip}", font=font, fill=255)
                    draw.text((0, 18),  f"CPU:  {cpu:>5.1f}%", font=font, fill=255)
                    draw.text((0, 36),  f"RAM:  {mem.percent:>5.1f}%", font=font, fill=255)
                else:
                    draw.text((0, 0),   f"Disk: {disk.percent:>5.1f}%", font=font, fill=255)
                    draw.text((0, 18),  f"Temp: {temp:>5.1f}°C", font=font, fill=255)
                    draw.text((0, 36),  f"Up:   {uptime_str}", font=font, fill=255)
        else:
            # Terminal fallback
            print(f"[Page {page}]")
            if page == 0:
                print(f"IP:   {ip}")
                print(f"CPU:  {cpu:.1f}%")
                print(f"RAM:  {mem.percent:.1f}%")
            else:
                print(f"Disk: {disk.percent:.1f}%")
                print(f"Temp: {temp:.1f}°C")
                print(f"Up:   {uptime_str}")
            print("-" * 30)

        page = (page + 1) % 2
        time.sleep(5)

    except Exception as e:
        print("[ERROR] Runtime exception:")
        print(traceback.format_exc())
        time.sleep(5)
