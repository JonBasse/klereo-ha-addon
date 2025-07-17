ARG BUILD_FROM
ARG BUILD_ARCH
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    curl \
    jq \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    bash

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages \
    requests \
    pyjwt \
    python-dateutil \
    aiohttp \
    schedule

# Skip Tempio installation for now

# Copy rootfs
COPY rootfs /

# Make executable
RUN chmod a+x /entrypoint.sh \
    && chmod a+x /usr/bin/klereo

# Set working directory
WORKDIR /usr/bin

# Use custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Labels
LABEL \
    io.hass.name="Klereo Pool Manager" \
    io.hass.description="Klereo pool management integration for Home Assistant" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="1.1.0"