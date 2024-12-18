FROM ubuntu:22.04

ENV BLENDER_MIRROR=https://mirror.clarkson.edu/blender/release/Blender3.6
ENV BLENDER_VERSION=3.6.2

# Install and setup blender
RUN apt-get update && \
    apt-get install -y \
       libxrender1 libxkbcommon-x11-0 libegl-dev xvfb libxi6 \
       wget unzip python3-numpy xz-utils && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /src/blender
RUN wget ${BLENDER_MIRROR}/blender-${BLENDER_VERSION}-linux-x64.tar.xz && \
    tar -xf blender-${BLENDER_VERSION}-linux-x64.tar.xz
ENV PATH="${PATH}:/src/blender/blender-${BLENDER_VERSION}-linux-x64"

# Add our source code
COPY . /src/TraitBlender
WORKDIR /src/TraitBlender

# Install the blender TraitBlender addon
RUN blender --background -E CYCLES --python dockersetup.py


# Setup default command to run a simple example
CMD blender --background -E CYCLES --python /src/TraitBlender/generate_dataset.py -- /src/TraitBlender/Examples/snails/make_snail.py /src/TraitBlender/Examples/snails/tiny_snails.csv '/src/TraitBlender/Examples/snails/traitblender_settings.json'

