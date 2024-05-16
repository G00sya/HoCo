FROM ubuntu:22.04

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# Add user
RUN adduser --quiet --disabled-password user && usermod -a -G user user

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Install Python 3, PyQt5
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install -y ffmpeg libsm6 libxext6
RUN apt-get install -y libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0
RUN apt-get install -y libxcb-xkb1 libxcb-shape0 libxkbcommon-x11-0 libxcb-xinerama0

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /src /app/src
COPY /static /app/static
COPY /build /app/build
COPY /examples /app/examples

# Clone CocoRPy3 repository and install CocoR
RUN cd build \
    git clone https://github.com/hb9chm/CocoRPy3 \
    cd CocoRPy3 \
    pip install build \
    python -m build \
    pip install ./dist/CocoRPy3-3.1.0-py3-none-any.whl \
    cd .. \
    coco ../src/parser/grammar.atg \
    python3 cocor_corrector.py \
    cd ..
