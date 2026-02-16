🖐️ AuraVolume: Gesture-Based Audio Control
AuraVolume is a Computer Vision project that allows you to control your Windows Master Volume using simple hand gestures. No more reaching for the keyboard—just pinch your fingers in the air to set the perfect vibe.

🚀 Features
Real-Time Hand Tracking: Powered by MediaPipe's 21-point landmark system.

Adaptive UI: A custom on-screen HUD with a dynamic color-changing volume bar.

Windows 11 Optimized: Specifically engineered to work with Realtek(R) Audio and Bluetooth devices like Airdopes.

Smart Filtering: Uses interpolation to ensure smooth volume transitions without "jitter."

🛠️ Tech Stack
Python (The backbone)

OpenCV: For real-time camera feed and UI rendering.

MediaPipe: For high-fidelity hand landmark detection.

PyCaw: To interface directly with the Windows Core Audio API.




Importand =====

py -3.11 -m venv venv

.\venv\Scripts\activate

