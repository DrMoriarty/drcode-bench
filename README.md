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

## Запуск

Матричный раннер (этап 5, план §8/§12): `scenarios × combos × repeats`,
один сценарий — один subprocess (изоляция `XDG_CONFIG_HOME`/`DRCODE_*`,
чистые импорты, никаких общих файлов и event loop — §2):

```bash
# вся матрица по всем сценариям S1–S6: 2 параллельных subprocess'а,
# 3 повтора на пару (медианы/разброс в отчёте); report.md строится сам
uv run bench run --scenario all --matrix matrix.toml --parallel 2 --repeats 3

# один сценарий / одна комбинация
uv run bench run --scenario s6_queue_priority --combo strong-coder/cheap-tester --repeats 1
```

- `--parallel` ограничивает одновременные subprocess'ы (rate limits
  провайдера / VRAM для локальных шлюзов).
- Инфраструктурные сбои (subprocess упал ДО старта приложения,
  недоступный провайдер на старте, pre-flight) повторяются: сначала
  перепроверка конфига, потом новый прогон в свежем `runs/<run_id>/`.
  Содержательный провал (таймаут, красный checks.py) — просто точка
  данных: не ретраится, попадает в отчёт (§8/§13).
- История планировщика — `runs/runner-summary.json`.

Одиночный прогон (этапы 1–3, §12):

```bash
# один прогон сценария на комбинации: env → headless DrCodeApp → settle (§4)
python -m bench.run_one s2a_bug_followup strong-coder/cheap-tester runs/s2a-r1

# внутри прогона работает симулятор пользователя (§6): авто-ответы на
# clarification, follow-up-комментарии, защита от залипания — все
# вмешательства пишутся в runs/<run_id>/user_sim.jsonl
```

Отчёт (§10): таблица combo × scenario — медиана wall-time, медиана/сумма
токенов per role, вердикт, число компакций, разброс по повторам
(min…max), колонка гейта «никакой девелопмент, пока идёт testing» (§7
S6); каждая ячейка кликабельно ссылается на `runs/<run_id>/`:

```bash
uv run bench report runs/            # → runs/report.md
uv run bench report runs/ --html     # + runs/report.html
```

## Структура

```
├── matrix.toml          # провайдеры + комбинации моделей по ролям (§8)
├── bench/
│   ├── __main__.py      # CLI: run / report
│   ├── runner.py        # матричный раннер: план → параллельные subprocess'ы (§8)
│   ├── run_one.py       # один прогон: env → DrCodeApp headless → settle (§4)
│   ├── recording.py     # recording-обёртка build_model (§5)
│   ├── user_sim.py      # симулятор пользователя (§6)
│   ├── settle.py        # критерий завершения + диагностика провала (§4)
│   ├── metrics.py       # парсинг .drcode/tasks/*.json + логов (§10)
│   └── report.py        # агрегация → markdown/HTML (§10)
├── scenarios/           # сценарии: seed/ + scenario.toml + checks.py (§7)
├── drcode/              # субмодуль — исходники drcode
└── runs/                # артефакты прогонов (gitignored)
```

## Тесты

```bash
uv run pytest
```
