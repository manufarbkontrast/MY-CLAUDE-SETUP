# Docker Cross-Platform Build: Apple Silicon to AMD64 Server

**Extracted:** 2026-03-06
**Context:** Deploying Docker images from Apple Silicon (M1/M2/M3) Macs to x86_64/AMD64 cloud servers (Hetzner, AWS, DigitalOcean, etc.)

## Problem

Docker images built on Apple Silicon Macs default to `linux/arm64` architecture. When transferred to an AMD64 server (most cloud VPS), the container fails immediately with:

```
exec /usr/local/bin/docker-entrypoint.sh: exec format error
```

The `docker load` step may show a warning but still loads the image:
```
WARNING: The requested image's platform (linux/arm64) does not match
the detected host platform (linux/amd64/v4)
```

## Solution

Always specify `--platform linux/amd64` when building images intended for cloud servers:

```bash
# Build for AMD64 (cloud servers)
docker build --platform linux/amd64 -t myapp:latest .

# Or make it configurable in deploy scripts
PLATFORM="${PLATFORM:-linux/amd64}"
docker build --platform "${PLATFORM}" -t "${IMAGE_NAME}:${IMAGE_TAG}" .
```

### Deploy Script Pattern

```bash
# Configurable platform with AMD64 as default (most cloud servers)
PLATFORM="${PLATFORM:-linux/amd64}"

log "Building ${IMAGE_NAME}:${IMAGE_TAG} (${PLATFORM}) ..."
docker build --platform "${PLATFORM}" -t "${IMAGE_NAME}:${IMAGE_TAG}" .
```

### Dockerfile Consideration

No Dockerfile changes needed. The `--platform` flag on `docker build` handles cross-compilation via QEMU emulation (built into Docker Desktop).

Build will be slower than native (2-3x) due to emulation, but the resulting image runs natively on the target architecture.

## Diagnosis

If a container exits immediately after starting on the server:

```bash
# Check container logs for exec format error
docker logs <container_name>

# Check image architecture
docker inspect <image_name> | grep Architecture
```

## When to Use

- Building Docker images on Apple Silicon Mac (M1/M2/M3/M4)
- Deploying to ANY cloud server (Hetzner, AWS EC2, DigitalOcean, Linode, etc.)
- Container starts but immediately exits with no useful application logs
- `exec format error` in container logs
