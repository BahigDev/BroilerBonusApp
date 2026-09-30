[app]
title = Broiler Bonus App
package.name = broilerbonus
package.domain = org.poultry
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0
requirements = python3,kivy==2.2.1,arabic_reshaper,python-bidi
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.accept_sdk_license = True
