[app]

# (str) Title of your application
title = Broiler Bonus App

# (str) Package name
package.name = broilerbonus

# (str) Package domain (needed for android/ios packaging)
package.domain = org.poultry

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (python, kv, etc)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = hostpython3,python3,kivy==2.2.1,arabic_reshaper,python-bidi

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) Android NDK architecture to build for
android.archs = arm64-v8a, armeabi-v7a


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0_No or 1_Yes)
warn_on_root = 1
