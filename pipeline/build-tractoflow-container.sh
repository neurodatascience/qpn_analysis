#!/bin/bash

# docker hub user ID - needs to be logged in
DHUSER=your-dh-user-name

# build the docker image w/ local Dockerfile
docker build -t $DHUSER/nipoppy-tractoflow .

# add a version tag
docker tag $DHUSER/nipoppy-tractoflow $DHUSER/nipoppy-tractoflow:2.4.2

# push the image to dockerhub to pull for apptainer build
docker push $DHUSER/nipoppy-tractoflow:2.4.2

# build the apptainer version of the image
apptainer build tractoflow_2.4.2.sif docker://$DHUSER/nipoppy-tractoflow:2.4.2
