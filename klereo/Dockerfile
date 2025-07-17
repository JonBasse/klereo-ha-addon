ARG BUILD_FROM
FROM $BUILD_FROM

# Install system dependencies including Python
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    jq \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    requests \
    pyjwt \
    python-dateutil \
    aiohttp \
    schedule

# Skip Tempio installation for now

# Copy rootfs
COPY rootfs /

# Make executable
RUN chmod a+x /etc/services.d/klereo/run \
    && chmod a+x /usr/bin/klereo

# Set working directory
WORKDIR /usr/bin

# Labels
LABEL \
    io.hass.name="Klereo Pool Manager" \
    io.hass.description="Klereo pool management integration for Home Assistant" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"