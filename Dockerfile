# Dockerfile for modern OpenKomodoIDE build environment
# Supports Python 3 and Firefox 140 ESR

FROM ubuntu:22.04

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    git \
    mercurial \
    subversion \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    autoconf2.13 \
    automake \
    libtool \
    pkg-config \
    curl \
    wget \
    unzip \
    zip \
    tar \
    gzip \
    bzip2 \
    xz-utils \
    patch \
    make \
    cmake \
    ninja-build \
    gcc \
    g++ \
    clang \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libffi-dev \
    liblzma-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libglib2.0-dev \
    libgtk-3-dev \
    libdbus-glib-1-dev \
    libgconf2-dev \
    libasound2-dev \
    libpulse-dev \
    libxt-dev \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxrandr-dev \
    libxfixes-dev \
    libxi-dev \
    libxcb1-dev \
    libxcb-render0-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    libxcb-randr0-dev \
    libxcb-shape0-dev \
    libxcb-keysyms1-dev \
    libxcb-icccm4-dev \
    libxcb-image0-dev \
    libxcb-util0-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    libwayland-dev \
    libegl1-mesa-dev \
    libgbm-dev \
    libdrm-dev \
    libgles2-mesa-dev \
    libvpx-dev \
    libopus-dev \
    libwebp-dev \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libevent-dev \
    libnss3-dev \
    libnspr4-dev \
    libsqlite3-dev \
    libffi-dev \
    libpixman-1-dev \
    libharfbuzz-dev \
    libgraphite2-dev \
    libicu-dev \
    libhunspell-dev \
    libhyphen-dev \
    libstartup-notification0-dev \
    libsecret-1-dev \
    libjsoncpp-dev \
    libdbus-1-dev \
    libatk1.0-dev \
    libatk-bridge2.0-dev \
    libepoxy-dev \
    libgudev-1.0-dev \
    libcolord-dev \
    libgtk-3-dev \
    libgdk-pixbuf2.0-dev \
    libpango1.0-dev \
    libcairo2-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    libgstreamer-plugins-ugly1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (required for modern Firefox builds)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Node.js (required for some build tools)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# Install Python dependencies
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install mercurial six

# Set up build environment
ENV DEBIAN_FRONTEND=noninteractive
ENV MOZCONFIG=/root/mozconfig
ENV MOZ_OBJDIR=/root/mozilla-objdir
ENV PYTHON=/usr/bin/python3

# Create build directories
RUN mkdir -p /root/build /root/mozilla /root/mozilla-objdir
WORKDIR /root/build

# Copy build scripts
COPY mozilla/build.py /root/build/
COPY util/black/bk.py /root/build/

# Set up entrypoint
COPY docker-entrypoint.sh /root/
RUN chmod +x /root/docker-entrypoint.sh

ENTRYPOINT ["/root/docker-entrypoint.sh"]
CMD ["bash"]