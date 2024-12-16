FROM ubuntu/bind9:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    dnsutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Set working directory
WORKDIR /app
VOLUME ["/etc/bind"]
RUN chown -R bind:bind /etc/bind && chmod -R 775 /etc/bind

# Copy configuration files
COPY dnssec /app
COPY bind.keys /etc/bind/bind.keys
COPY db.example.com /etc/bind/db.example.com
COPY db.forward /etc/bind/db.forward
COPY db.local /etc/bind/db.local
COPY db.resolverinfo /etc/bind/db.resolverinfo
COPY db.root /etc/bind/db.root
COPY dsset-example.com /etc/bind/dsset-example.com.
COPY managed-keys.bind /etc/managed-keys.bind
COPY named.conf /etc/bind/named.conf
COPY named.conf.default-zones /etc/bind/named.conf.default-zones
COPY named.conf.local /etc/bind/named.conf.local
COPY named.conf.options /etc/bind/named.conf.options
COPY rndc.key /etc/bind/rndc.key

# Create virtual environment and install dependencies
RUN python3 -m venv venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt
# Expose ports
EXPOSE 5000 53/udp 53/tcp

# Health check to verify DNS service
HEALTHCHECK --interval=30s --timeout=10s \
  CMD dig @localhost example.com || exit 1

# Run BIND9 in foreground
CMD ["/usr/sbin/named", "-f", "-g"]