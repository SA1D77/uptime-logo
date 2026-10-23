#!/bin/bash
# Обновление Uptime Kuma (Asvad Logistic) на сервере.
#   ./update-kuma.sh          — последняя собранная версия
#   ./update-kuma.sh 2.5.6    — конкретная версия (в том числе для отката)
set -e
IMG=ghcr.io/sa1d77/uptime-kuma-asvad
TAG="${1:-latest}"

docker pull "$IMG:$TAG"
CUR=$(docker exec uptime-kuma node -p "require('./package.json').version" 2>/dev/null || echo "?")
NEW=$(docker run --rm --entrypoint node "$IMG:$TAG" -p "require('./package.json').version")
echo "Сейчас запущена: $CUR"
echo "Будет установлена: $NEW"
read -p "Продолжить? (y/n) " A
[ "$A" = "y" ] || exit 1

docker stop uptime-kuma
sudo cp -a /var/lib/docker/volumes/uptime-kuma/_data ~/kuma-backup-$(date +%F-%H%M)
docker rm -f uptime-kuma-old 2>/dev/null || true
docker rename uptime-kuma uptime-kuma-old
docker run -d --name uptime-kuma --network kuma-net --restart unless-stopped \
  -p 127.0.0.1:3001:3001 -v uptime-kuma:/app/data "$IMG:$TAG"
sleep 25
docker ps --filter name=uptime-kuma
echo "Готово: https://monitor.asvadlogistic.uz (лучше открыть в инкогнито)."
echo "Если что-то не так — откат: docker rm -f uptime-kuma && docker rename uptime-kuma-old uptime-kuma && docker start uptime-kuma"
