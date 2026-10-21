# Сценарии

Формат сценария — план `drcode-bench.md` §7. Один сценарий = одна папка
`scenarios/<id>/`:

```
scenarios/s1_happy/
├── seed/                  # сид-репозиторий: код + тесты, копируется в workspace
├── scenario.toml          # briefs, followups, clarification_answers, timeout
├── AGENTS.md              # (опция) проектные инструкции для агентов
└── checks.py              # механическая проверка результата (вызывается харнессом)
```

## seed/

Маленький репозиторий (пара файлов, 1–2 теста): цель бенчмарка —
взаимодействия и тайминги, а не сложность задачи. Сид содержит проверяемый
контракт («функция X проходит тест Y»): харнесс после прогона **сам запускает
pytest в workspace**, вердикт не строится на словах агентов.

- kinds задач — только `feature`/`bug` (research не проходит тестера).
- Для сценариев с багами (S2a/S2b) сид содержит заведомо сломанный код и
  тест, который его ловит.
- Для S4 в сиде лежит файл с десятками тысяч строк, а brief велит
  «проверь полный листинг X» — чтобы тестер был вынужден читать жирный вывод.

## scenario.toml

- `briefs` — задачи: title, text, kind.
- `followups` — комментарии симулятора пользователя по условию
  (верификация failed / elapsed / событие).
- `clarification_answers` — ответы на clarification (матч по тексту вопроса
  или по порядку).
- `timeout` — мягкий предел сценария (30–60 мин), по истечении — провал
  с диагностикой.
- `[settle]` — сценарно-специфичная часть settle-критерия (§4):
  `verification = "passed"` требует, чтобы целевые задачи завершились
  с меткой PASSED тестировщика (`"any"` — метка не проверяется).

## checks.py

Вызывается харнессом после прогона (`bench/run_one.py`, §4): контракт —

    python checks.py <workspace>     # exit 0 = зелёный

Механическая проверка результата (обычно — прогон pytest сидовых тестов
в workspace плюс assertions по task-JSON: `verification`, число
testing-раундов, события компакции). Вердикт никогда не строится на
словах агентов. Провал checks.py = провал прогона, даже если
settle-критерий был достигнут.

## Каталог сценариев (план §7)

S1 happy path · S2a bug→follow-up · S2b bug-report тестера · S3 компакция
у кодера · S4 компакция у тестера · S5 clarification · S6 очередь ·
S7 fault injection (опция).

Реализованы: S1, S2a, S2b, S5 (этапы 1–3), **S3, S4 (этап 4)**.

## Интерактивные сценарии этапа 3 (план §6/§7)

- `s2a_bug_followup/` — seeded bug: тестер ставит FAILED, симулятор
  пользователя (§6) отправляет follow-up «вот лог ошибки, исправь»
  (текст — из сценария), второй раунд чинит и завершается PASSED.
  Assertions checks.py: ≥2 testing-раунда, финально PASSED, follow-up
  виден в транскрипте кодера ровно одним prompt'ом (без дублей).
- `s2b_bug_report/` — бриф подталкивает тестера к `create_bug_report` на
  дефекте вне объёма задачи; баг-задача (kind=bug) выполняется раньше
  прочих в очереди (по `activated_at` — bugs newest-first в
  `TaskManager.queued()`), обе brief-задачи COMPLETED, баг-задача прошла
  testing (PASSED).
- `s5_clarification/` — brief требует данных, которых нет в репозитории:
  кодер вызывает `ask_clarifying_question`, симулятор отвечает через
  `TaskManager.send()` (голова очереди). Assertions checks.py: ответ
  потреблён ровно одним prompt'ом (нет дублей — проверка через логику
  `is_pending_retry`), ответ не остался в `pending_input`, цепочка
  clarification→queued→completed подтверждена записью в `user_sim.jsonl`
  (действие `clarification_answer` в статусе `clarification`).

Симулятор пользователя (`bench/user_sim.py`, §6) подключён в
`bench/run_one.py`: asyncio-таск в том же loop, опрос `app.manager` раз в
0.75 с, все мутации — только публичный API `TaskManager` (тот же, что
использует TUI); каждое действие пишется в `runs/<run_id>/user_sim.jsonl`,
провалы сценария (нет ответа на clarification, залипание ACTIVE без
работы) — жёсткий settle-blocker. `metrics.json` агрегирует
`user_sim_interventions`, отчёт добавляет колонки «вмешательств
симулятора» и «bug round-trip'ов».

## Компакционные сценарии S3/S4 (этап 4, план §1.2/§12)

- «Маленький контекст» ставится **кодинговой** модели: либо отдельным id
  модели в каталоге (`qwen3-8b-small-ctx`), либо переопределением на роль
  из combo — `coding_max_context_tokens = 3000` в matrix.toml (попадает в
  entry каталога models.json, который перекрывает flat config для роли;
  env `DRCODE_MAX_CONTEXT_TOKENS` не используется и в прогоне вычищается).
- S3: сид — каталог `glossary/` из 18 модулей, brief велит прочитать
  каждый; assertions checks.py: событие «Context compacted», compaction
  start (mid-run pause или turn boundary), `COMPACTION_SUMMARY_PREFIX`
  в `messages`, исходный user-промпт дословно, задача COMPLETED/PASSED,
  pytest зелёный.
- S4: сид — `data/listing.txt` на 25 000 строк, brief велит «проверь
  полный листинг» (run_bash с жирным stdout); assertions checks.py:
  compaction-евент внутри testing-раунда, `tester_messages[-1]` содержит
  summary, вердикт выставлен.
- Источник порога тестера (§1.2/§13: конфиг КОДИНГОВОЙ модели) — объект
  проверки: `metrics.json` классифицирует его
  (`tester_threshold_from_coding`), отчёт помечает регрессию.
- `metrics.json` также содержит: `repeat_compaction` (повторная компакция
  — деградация после summary) и `compaction_failed`-евенты (в drcode
  failure компакции never fatal: gate отключается, ран продолжается
  несжатым; отчёт помечает это состояние).
- Деградационная combo «слабого компактизатора» — `degradation-weak-compactor`
  в matrix.toml (ручная проверка); полный матричный раннер — этап 5.

Этапы 4–5 плана (§12) наполняют остальные сценарии и матричный раннер.
