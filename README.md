# space-invaders
Pattern recognition in a 2D matrix

## Installation
### Install and run via docker

```shell
docker buildx build -t space-invaders:latest . --load=true
docker run --rm space-invaders:latest
```

### Install and run manually

#### Install
```shell
python -m pip install --user -e .
python -m pip install --user -e '.[all]'  # Or with tests.
python -m space_invaders
```


## Run tests
### Via Python script:
```shell
python -m pytest
```
### Via docker:
```shell
docker run -it --rm space-invaders:latest pytest
```
