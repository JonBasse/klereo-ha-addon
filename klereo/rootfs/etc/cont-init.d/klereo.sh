#!/usr/bin/with-contenv bashio
# ==============================================================================
# Klereo Pool Manager Add-on
# Prepares the Klereo Pool Manager for running
# ==============================================================================

bashio::log.info "Preparing Klereo Pool Manager..."

# Create necessary directories
mkdir -p /var/log

# Set proper permissions
chown -R root:root /usr/bin/klereo*
chmod +x /usr/bin/klereo*

bashio::log.info "Klereo Pool Manager prepared!"