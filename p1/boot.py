import storage
import usb_cdc
import usb_midi

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "player1"  # Change "MyDevice" to whatever name you want

usb_cdc.enable(console=True, data=True)
usb_midi.enable()
