cd /home/shubham/image-to-text
echo $USER >> textfile.txt
export XDG_RUNTIME_DIR=/run/user/1001
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1001/bus


systemctl --user restart app

