# Item ???

> some description

## Requirements

Note: This should have requirements in a virtualenv but it's scav, so ain't nobody got time for that.

### Video Player

1. python-omxplayer-wrapper

```
# Prereqs
sudo apt-get update && sudo apt-get install -y libdbus-1{,-dev}

# Install the package
pip3 install omxplayer-wrapper
```

(Or follow the installation instructions here: http://python-omxplayer-wrapper.readthedocs.io/en/latest/)

Gotchas:

- The OMXPlayer wrapper can only have one video per instance as per https://github.com/willprice/python-omxplayer-wrapper/issues/73 thus we work around this by concatenating all of our videos together and simply seekingto play different snippets.

