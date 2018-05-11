# (in progress) What actually worked

- Seems like our remote wasn't working and `irrecord` command with 0.9.4c might be messed up?
- Got the file using `irdb-get find samsung` then installed the closest match to our tv remote (not the starter kit remote) and copied to `/etc/lirc/lircd.conf.d/`
- irw worked then for the good config!! a good way to debug this moving forward is to use a config and remote already known to work

# (OUTDATED) Some useful commands, files, and directories

## Commands

```
sudo systemctl status lircd.service
sudo systemctl start lircd.service
sudo systemctl stop lircd.service

sudo /etc/init.d/lircd stop
sudo /etc/init.d/lircd start
```

## Directories & Files

```
# "only config for lirc for 0.9.4c"
/boot/config.txt

# Directory to put config files
/etc/lirc/lircd.conf.d/

# File that needs to be renamed if default distro conf doesn't work
# See more: cat /etc/lirc/lircd.conf.d/README.conf.d
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.dist

# probably don't touch these files moving forward
/etc/lirc/lirc_options.conf
/etc/lirc/hardware.conf
/etc/modules
```

## Files in this repo

- `elago1.lirc.conf` we generated this for our remote
- the other files are to debug if there is a bug in the generation code

