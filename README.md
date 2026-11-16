# refro — вёрстка на базовых стилях refro.ru

Песочница для вёрстки блоков/страниц под сайт [refro.ru](https://www.refro.ru/) (Bitrix + шаблон **Aspro Max**).
Все CSS сайта скачаны локально, чтобы новая вёрстка сразу выглядела «как на сайте». Свои стили пишем отдельно, стили сайта не трогаем.

Скачано: 13.11.2026.

## Быстрый старт

```bash
cd "/Volumes/SSD 1TB/Work/verstka_fouro/refro"
python3 -m http.server 8765
```

Открыть: http://localhost:8765/index.html

Можно и просто открыть `index.html` двойным кликом, но шрифты через `file://` иногда не грузятся — лучше через сервер.

## Структура

```
refro/
├── index.html              # шаблон страницы с обёртками сайта, подключает bundle + style.css
├── css/
│   ├── refro.bundle.css    # ВСЕ стили сайта одним файлом (~1.5 МБ) — НЕ ТРОГАТЬ
│   ├── style.css           # СВОИ стили пишем сюда
│   └── refro/
│       ├── 00-inline.css … 12-print.css   # те же стили по отдельным файлам (порядок = как на сайте)
│       └── assets/         # шрифты, картинки, спрайты; url() в CSS переписаны на локальные
└── tools/
    ├── grab_refro.py       # перекачать все стили с сайта заново
    └── retry_assets.py     # докачать недостающие ассеты
```

`refro.bundle.css` и `css/refro/*.css` — одно и то же. Подключать **что-то одно**: либо bundle (как сейчас в `index.html`), либо отдельные файлы по порядку `00 → 12`.

## Что внутри стилей

| Файл | Что это |
|---|---|
| `00-inline.css` | inline-переменные со страницы: `--theme-base-color: #f6de63`, `--theme-page-width: 1500px` и др. |
| `01-ui.design-tokens.css` | Bitrix UI design tokens |
| `02-ui.font.opensans.css` | Bitrix OpenSans |
| `03-main.popup.bundle.css`, `09-panel.popup.css` | Bitrix popup'ы |
| `04/05-default_*.css`, `07-template_cd74.css` | кешированные куски компонентов Bitrix |
| `06-bonus-system.css` | бонусная система |
| `08-template_6af1.css` | **основной шаблон Aspro Max** (~1.4 МБ): сетка, кнопки, шапка, каталог, всё остальное |
| `10-critical.css` | critical (почти пустой) |
| `11-HelveticaNeueCyr.css` | основной шрифт сайта HelveticaNeueCyr |
| `12-print.css` | `@media print` |

**Не взято специально**: CSS сторонних виджетов — Searchbooster (поиск, классы `.l-ss-c-*`) и Mango (виджет звонков, ~1.9 МБ inline). К вёрстке не относятся.

## Как верстать

### Обёртки обязательны

Стили Aspro Max сильно завязаны на родительские классы. Вёрстку класть **внутрь цепочки** из `index.html`:

```
body#main.site_s1.theme-light ...
└── .wrapper1.<модификаторы шаблона>
    └── #content.wraps
        └── .wrapper_inner.wide_page
            └── .container_inner.clearfix
                └── .middle
                    └── .maxwidth-theme      ← сюда свой контент
```

Если блок вынести за эти обёртки — часть стилей не применится.

- **Внутренняя страница** — как сейчас в `index.html`.
- **Главная** — добавить `front_page` в `.wrapper1` и `front` в `.wrapper_inner` (на сайте так).

### Что уже есть из коробки

- Сетка Bootstrap 3: `.row`, `.col-xs-* / .col-sm-* / .col-md-* / .col-lg-*` (брейкпоинты 768 / 992 / 1200).
- Кнопки: `.btn.btn-default` (жёлтая), `.btn.btn-default.white`, `.btn.btn-transparent-border-color` и др.
- Контейнер `.maxwidth-theme` (ширина берётся из `--theme-page-width`).
- Типографика h1–h6, списки (маркер `—`), ссылки и т.д.
- Утилиты Aspro: `.flexbox`, `.flexbox--gap-16`, `.visible-xs/sm/md/lg`, `.hidden-*` и пр.

Если нужен существующий блок сайта, проще всего открыть refro.ru → DevTools → скопировать HTML блока вместе с классами → вставить в `.maxwidth-theme`. Стили подхватятся.

### Свои стили

Только в `css/style.css` (подключён после bundle, поэтому перебивает). Чтобы не конфликтовать с классами шаблона, свои классы лучше префиксить, например `.rf-*`.

## Обновить стили с сайта

Если на refro.ru поменялись стили:

```bash
python3 tools/grab_refro.py      # качает CSS, вытаскивает url() в assets/, пересобирает bundle
python3 tools/retry_assets.py    # докачивает то, что упало по таймауту
```

Нюансы:

- **Сайт за защитой Qrator.** HTML-страница через curl отдаёт JS-заглушку, но статику (`.css`, шрифты, картинки) отдаёт нормально — скрипты качают только статику.
- **Не качать параллельно.** Qrator на время банит IP (запросы виснут по таймауту). Скрипты специально качают по одному с паузой. Если всё таймаутит — подождать пару минут и запустить `retry_assets.py`.
- **Имена файлов кеша Bitrix меняются.** Файлы вида `/bitrix/cache/css/s1/aspro_max/template_<хеш>/...` при обновлении сайта получают новый хеш, и старые URL в `tools/grab_refro.py` (список `CSS`) начнут отдавать 404. Актуальный список взять в консоли браузера на refro.ru:

  ```js
  [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.href).join('\n')
  ```

  и обновить список `CSS` в скрипте. Inline-переменные темы (`INLINE` в скрипте) смотреть там же:

  ```js
  [...document.querySelectorAll('style')].filter(s => s.textContent.length < 20000).map(s => s.textContent)
  ```

## Известные битые ссылки

12 `url()` в CSS сайта ведут на файлы, которых нет на самом refro.ru (404): `basket_icons.png`, `arrows_big.png`, `arrows_small.png` (по двум путям), `css/images/arrows.png`, `eye_open.svg`, `eye_close.svg`, `burger_white.svg`, `trianglearrows.svg`, `bonus_icon_white.svg`, `cookiesaccept/.../style-1-2.svg`, `css/image_source` (401). Это мёртвые ссылки в их CSS, на вёрстку не влияет — не чинить.
