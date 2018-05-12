# (in progress) What actually worked

- Seems like our remote wasn't working and `irrecord` command with 0.9.4c might be messed up?
- Got the file using `irdb-get find samsung` then installed the closest match to our tv remote (not the starter kit remote) and copied to `/etc/lirc/lircd.conf.d/`
- irw worked then for the good config!! a good way to debug this moving forward is to use a config and remote already known to work

# TODO actually document this

## resources used

- https://github.com/josemotta/IoT.Starter.Api/tree/master/gpio-base
- https://wiki.archlinux.org/index.php/LIRC#Example
- https://wiki.archlinux.org/index.php/LIRC#Configuration

## what we did

1. install stuff

```
# todo: break this into multi line with \
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y lirc && sudo rm -rf /var/lib/apt/lists/*
```

2. double check your version

NOTE: no promises that this will work if you are not using lircd 0.9.4c

```
# Double check that your output looks like this
$ lircd --version
lircd 0.9.4c
```

3. update lirc_options.conf

```
sudo nano /etc/lirc/lirc_options.conf
```

Change `device` and `driver` to the following

```
driver          = default
device          = /dev/lirc0
```

4. update /boot/config.txt

Add this line:

```
dtoverlay=lirc-rpi,gpio_out_pin=17,gpio_in_pin=18,gpio_in_pull=up
```

The dtoverlay part of our config looks like this now:

```
# Uncomment this to enable the lirc-rpi module
#dtoverlay=lirc-rpi
dtoverlay=lirc-rpi,gpio_out_pin=17,gpio_in_pin=18,gpio_in_pull=up
```

5. Restart

```
sudo reboot
```

6. Check lircd status

```
$ /etc/init.d/lircd status
```

Our output looks like this which works even though there are warnings

```
$ /etc/init.d/lircd status
● lircd.service - Flexible IR remote input/output application support
   Loaded: loaded (/lib/systemd/system/lircd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2018-05-11 21:20:53 UTC; 53min ago
     Docs: man:lircd(8)
           http://lirc.org/html/configure.html
 Main PID: 1728 (lircd)
   CGroup: /system.slice/lircd.service
           └─1728 /usr/sbin/lircd --nodaemon

May 11 21:26:24 raspberrypi lircd-0.9.4c[1728]: Notice: accepted new client on /var/run/lirc/lircd
May 11 21:26:24 raspberrypi lircd-0.9.4c[1728]: Info: Cannot configure the rc device for /dev/lirc0
May 11 21:26:50 raspberrypi lircd[1728]: lircd-0.9.4c[1728]: Info: removed client
May 11 21:26:50 raspberrypi lircd-0.9.4c[1728]: Info: removed client
May 11 21:45:56 raspberrypi lircd[1728]: lircd-0.9.4c[1728]: Notice: accepted new client on /var/run/lirc/lircd
May 11 21:45:56 raspberrypi lircd[1728]: lircd-0.9.4c[1728]: Info: Cannot configure the rc device for /dev/lirc0
May 11 21:45:56 raspberrypi lircd-0.9.4c[1728]: Notice: accepted new client on /var/run/lirc/lircd
May 11 21:45:56 raspberrypi lircd-0.9.4c[1728]: Info: Cannot configure the rc device for /dev/lirc0
May 11 21:46:18 raspberrypi lircd[1728]: lircd-0.9.4c[1728]: Info: removed client
May 11 21:46:18 raspberrypi lircd-0.9.4c[1728]: Info: removed client
```

7. Run `irw` then press a bunch of buttons to see if things work

If there is output, things are working. Otherwise, it's probably your .conf file.
Should be a step above -- Make sure you have a valid conf file in /etc/lirc/lircd.conf.d/
Should be another step above -- run this: 

```
# See more: cat /etc/lirc/lircd.conf.d/README.conf.d
sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.dist
```

Then restart (you can also just restart lircd but it's easier to reboot then check the status).

If none of this works, seriously, get another remote, check `irdb-get find $SOME_REMOTE_NAME_SUBSTRING` and move THAT conf file to /etc/lirc/lircd.conf.d/, then see if that remote works. `irrecord` seems to have problems with 0.9.4c

## Troubleshooting

If you see an output like this in the commandline:

```
$ <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999992222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222^C
```

something's kind of messed up. I'm not sure what the issue actually is, but it has something to do with way too many processes running

```
$ ps aux | grep lirc
root       321  0.0  0.1   4280  1112 ?        Ss   02:23   0:00 /usr/sbin/lircmd --nodaemon
root       335  0.0  0.1   4208  1080 ?        Ss   02:23   0:00 /usr/bin/irexec /etc/lirc/irexec.lircrc
root       408  0.0  0.3   7192  3208 ?        Ss   02:23   0:00 /usr/sbin/lircd --nodaemon
root       410  0.0  0.1   4284  1156 ?        Ss   02:23   0:00 /usr/sbin/lircd-uinput
pi         851  0.0  0.0   4372   560 pts/0    S+   02:26   0:00 grep --color=auto lirc
```

so kill and then start `lircd` (commands below)

```
sudo /etc/init.d/lircd stop
sudo /etc/init.d/lircd start
```

If the restart worked, your processes should look like this:

```
$ ps aux | grep lirc
root       953  0.1  0.3   7192  3152 ?        Ss   02:27   0:00 /usr/sbin/lircd --nodaemon
pi         975  0.0  0.0   4372   580 pts/0    S+   02:28   0:00 grep --color=auto lirc
```

and you should be good to go.

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

