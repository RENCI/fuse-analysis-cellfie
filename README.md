# fuse-analysis-cellfie
The fuse-style analysis module for the CellFIE systems biology models

# install:
```
git clone --recursive http://github.com/RENCI/fuse-analysis-cellfie.git
```
Be sure docker and python are properly installed, see docs [here](https://github.com/RENCI/pdspi-fhir-example/tree/master/doc) might help.

# start:
Then run:
```
./up.sh
```

# down:
```
./down.sh
```

# test:

Ensure there's no collision with the port:
```
curl -X GET  http://localhost:8080/config
```
