# Multilevel Compression File Generator

## Usage
* Set .env variables from .env.sample
* Set COMPRESSION_LEVEL to 5 to test for 5 level deep nesting.

## Build

    `To build the Docker image and name it `multilevel-compression` 

    `docker build -t multilevel-compression .`


## To run

    `docker run --env-file .env multilevel-compression`
