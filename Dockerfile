FROM ubuntu:22.04

WORKDIR /app

#ENV DEBIAN_FRONTEND=noninteractive

# Add user
#RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# This fix: libGL error: No matching fbConfigs or visuals found
#ENV LIBGL_ALWAYS_INDIRECT=1



RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY /src /app

#ENV PYTHONPATH /app
#ENV PIP_DISABLE_PIP_VERSION_CHECK 1
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#ENV QT_QPA_PLATFORM_PLUGIN_PATH /app


#RUN apt-get update #&& apt-get install -y git && \
#      git clone https://github.com/hb9chm/CocoRPy3 && \
#      cd CocoRPy3 && \
#      pip install build && \
#      python3 -m build && \
#      pip install ./dist/CocoRPy3-3.1.0-py3-none-any.whl && \
#      coco ../parser/grammar.atg

#
#
#RUN apt-get install -y libgl1-mesa-glx && \
#    apt-get install -y libglib2.0-dev && \
#    apt-get install -y libxcb-icccm4 && \
#    apt-get install -y libxcb-image0

