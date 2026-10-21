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

Одиночный прогон (этапы 1–3, §12):

```bash
# один прогон сценария на комбинации: env → headless DrCodeApp → settle (§4)
python -m bench.run_one s2a_bug_followup strong-coder/cheap-tester runs/s2a-r1

# внутри прогона работает симулятор пользователя (§6): авто-ответы на
# clarification, follow-up-комментарии, защита от залипания — все
# вмешательства пишутся в runs/<run_id>/user_sim.jsonl
```

## Структура

```
├── matrix.toml          # провайдеры + комбинации моделей по ролям (§8)
├── bench/
│   ├── __main__.py      # CLI: run / report
│   ├── run_one.py       # один прогон: env → DrCodeApp headless → settle (§4)
│   ├── recording.py     # recording-обёртка build_model (§5)
│   ├── user_sim.py      # симулятор пользователя (§6)
│   ├── settle.py        # критерий завершения + диагностика провала (§4)
│   ├── metrics.py       # парсинг .drcode/tasks/*.json + логов (§10)
│   └── report.py        # агрегация → markdown (§10)
├── scenarios/           # сценарии: seed/ + scenario.toml + checks.py (§7)
├── drcode/              # субмодуль — исходники drcode
└── runs/                # артефакты прогонов (gitignored)
```

## Тесты

```bash
uv run pytest
```
