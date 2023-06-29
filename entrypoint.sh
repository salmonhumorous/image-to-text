export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1001/bus
export XDG_RUNTIME_DIR=/run/user/1001
cd /home/shubham/image-to-text
echo $USER >> textfile.txt
systemctl --user restart app

