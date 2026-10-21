# drcode-bench

Бенчмарк полной связки агентов [drcode](https://github.com/DrMoriarty/drcode):
**coding → testing → compaction** и всех межагентных взаимодействий, когда
каждому агенту назначена своя модель. План реализации —
[`drcode-bench.md`](drcode-bench.md).

drcode подключается как git-субмодуль (`./drcode`) и ставится как path-зависимость.

## Установка

```bash
uv sync                     # создаст .venv, поставит drcode (субмодуль), textual, rich, pytest
```

Субмодуль нужен обязательно:

```bash
git submodule update --init --recursive
```

## Запуск (плейсхолдеры — этап 1, §12 п.1)

```bash
# прогон сценария на комбинации моделей из matrix.toml
uv run bench run --scenario s1_happy --combo baseline-single-model --matrix matrix.toml

# агрегированный отчёт по прогонам
uv run bench report runs/
```

Подкоманды `run` / `report` на этапе 1 — заглушки: каркас CLI и
подготовка среды (`bench/env_setup.py`) уже работают, оркестратор
прогона (`bench/run_one.py`, headless `DrCodeApp`) подключается на
следующем этапе.

## Структура

```
├── matrix.toml          # провайдеры + комбинации моделей по ролям (§8)
├── bench/
│   ├── __main__.py      # CLI: run / report
│   ├── matrix.py        # парсинг matrix.toml, Combo, подстановка env:KEY
│   └── env_setup.py     # tmp-дерево прогона: models.json, drcode.json, settings.json, git (§3)
├── scenarios/           # сценарии: seed/ + scenario.toml + checks.py (§7)
├── drcode/              # субмодуль — исходники drcode
└── runs/                # артефакты прогонов (gitignored)
```

## Тесты

```bash
uv run pytest
```
