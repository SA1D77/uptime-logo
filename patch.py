# Заменяет логотип и надписи Uptime Kuma на Asvad Logistic.
# Запуск из корня исходников uptime-kuma: python3 ../patch.py
import json, os, pathlib, re, sys

BRAND = "Asvad Logistic"
TITLE = "Asvad Logistic Monitoring"
REPO_URL = "https://github.com/" + os.environ.get("GITHUB_REPOSITORY", "SA1D77/uptime-logo")

T = r'(?:\{\{ \$t\("Uptime Kuma"\) \}\}|Uptime Kuma)'
L40 = f'<img src="/logo.png" alt="{BRAND}" class="ms-4" style="height: 40px; width: auto;" />'
L32 = f'<img src="/logo.png" alt="{BRAND}" style="height: 32px; width: auto;" />'
L64 = f'<img src="/logo.png" alt="{BRAND}" style="height: 64px; width: auto;" />'
L200 = f'<img src="/logo.png" alt="{BRAND}" class="my-4" style="max-height: 200px; max-width: 300px;" />'

errors = []


def sub(path, pat, rep, required=False):
    p = pathlib.Path(path)
    s, n = re.subn(pat, lambda m: rep, p.read_text(encoding="utf-8"))
    p.write_text(s, encoding="utf-8")
    print(f"{path}: {n}")
    if required and n == 0:
        errors.append(f"{path}: {pat}")


desk = r'<object class="bi me-2 ms-4" width="40" height="40" data="/icon.svg" />\s*<span class="fs-4 title">' + T + r"</span>"
mob = r'<object class="bi" width="40" height="40" data="/icon.svg" />'
span = r'\s*<span class="fs-4 title ms-2">' + T + r"</span>"
upstream_releases = r'href="https://github\.com/louislam/uptime-kuma/releases"'

# Шапка и мобильное меню
sub("src/layouts/Layout.vue", desk, L40, True)
sub("src/layouts/Layout.vue", mob, L32, True)
sub("src/layouts/Layout.vue", span, "")
# Кнопка «New Update» ведёт на ваш репозиторий с инструкцией обновления
sub("src/layouts/Layout.vue", upstream_releases, f'href="{REPO_URL}#обновление"')

# Страница 404
sub("src/pages/NotFound.vue", desk, L40)
sub("src/pages/NotFound.vue", mob, L32)
sub("src/pages/NotFound.vue", span, "")

# Первичная настройка
sub("src/pages/Setup.vue", r'<object width="64" height="64" data="/icon.svg" />', L64, True)
sub("src/pages/Setup.vue", r'\s*<div style="font-size: 28px; font-weight: bold; margin-top: 5px">Uptime Kuma</div>', "")

# Настройки → О программе
about = "src/components/settings/About.vue"
sub(about, r'<object class="my-4" width="200" height="200" data="/icon.svg" />', L200, True)
sub(about, r'<div class="fs-4 fw-bold">Uptime Kuma</div>',
    f'<div class="fs-4 fw-bold">{TITLE}</div>\n'
    f'            <div class="text-muted small">на основе <a href="https://github.com/louislam/uptime-kuma" target="_blank" rel="noopener">Uptime Kuma</a> (MIT)</div>',
    True)
sub(about, upstream_releases + r'(\s*target="_blank" rel="noopener">)\s*\{\{ \$t\("Check Update On GitHub"\) \}\}',
    f'href="{REPO_URL}" target="_blank" rel="noopener">\n                    Сборка {BRAND} на GitHub (логотип и обновление)', True)

# Вкладка браузера
sub("index.html", r"<title>\s*Uptime Kuma\s*</title>", f"<title>{TITLE}</title>", True)
sub("index.html", r'content="Uptime Kuma monitoring tool"', f'content="{BRAND} monitoring"')
# Иконка вкладки остаётся /icon.svg — он квадратный и берётся из branding/

# Имя приложения при установке как PWA
m = pathlib.Path("public/manifest.json")
data = json.loads(m.read_text(encoding="utf-8"))
data.update(name=TITLE, short_name=BRAND, description=f"{BRAND} monitoring")
m.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
print("public/manifest.json: ok")

if errors:
    sys.exit("ОШИБКА: не найдены блоки (в новой версии изменилась разметка):\n  " + "\n  ".join(errors))
