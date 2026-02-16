import cv2
import numpy as np
import math
import comtypes
from HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# --- 🚀 THE ULTIMATE LAPTOP SPEAKER FIX ---
def get_volume_control():
    try:
        # 1. Initialize COM (Prepares Windows for the request)
        comtypes.CoInitialize()
        
        # 2. Local import to ensure the library is loaded after pip fix
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        # 3. Target the default audio output (your Laptop Speakers)
        devices = AudioUtilities.GetSpeakers()
        
        # 4. Activate the volume interface using its internal ID
        # This is the most stable way to bypass "Access Denied" or "AttributeError"
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        
        return cast(interface, POINTER(IAudioEndpointVolume))
    except Exception as e:
        print(f"⚠️ Primary Method failed: {e}")
        try:
            # Fallback for specific Windows 11 driver versions
            from pycaw.pycaw import IAudioEndpointVolume
            interface = devices.QueryInterface(IAudioEndpointVolume)
            return cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e2:
            print(f"❌ Connection failed: {e2}")
            return None

# Initialize Volume
volume = get_volume_control()
if volume:
    vol_range = volume.GetVolumeRange()
    min_vol, max_vol = vol_range[0], vol_range[1]
    print("✅ SUCCESS! Realtek Speakers Connected.")
else:
    print("❌ STILL FAILING. Make sure your Laptop Speakers are set to DEFAULT.")
    exit()

# --- ✨ UI SETUP ---
cap = cv2.VideoCapture(0)
detector = HandDetector(detection_con=0.8, max_hands=1)

while True:
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1) 
    img = detector.find_hands(img)
    lm_list = detector.get_positions(img)

    if len(lm_list) != 0:
        # Landmark 4: Thumb Tip | Landmark 8: Index Tip
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]
        
        # Visual Markers
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        
        # Interpolation: Map finger distance to Volume range
        vol_per = np.interp(length, [30, 180], [0, 100])
        vol_raw = np.interp(vol_per, [0, 100], [min_vol, max_vol])

        try:
            volume.SetMasterVolumeLevel(vol_raw, None)
        except:
            pass 

        cv2.putText(img, f'VOL: {int(vol_per)}%', (40, 450), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()