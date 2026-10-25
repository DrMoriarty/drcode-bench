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
S7 fault injection (опция) · S8 tester fix loop · S9 research-подсчёт.

Реализованы: S1, S2a, S2b, S5 (этапы 1–3), **S3, S4 (этап 4)**,
**S6, S7 (этапы 5–6), S8 (fix-loop), S9 (research V1)**.

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

- «Маленький контекст» ставится **целевой роли** (план §1.2, drcode ≥ 0.5.0 —
  пер-ролевое разрешение моделей): S3 — кодинговой модели (её mid-run/
  turn-boundary гейты), S4 — модели тестера (её mid-round гейт). Варианты:
  отдельный id модели в каталоге (`qwen3-8b-small-ctx`) либо переопределение
  на роль из combo — `<роль>_max_context_tokens = 3000` в matrix.toml
  (попадает в entry каталога models.json, который перекрывает flat config
  для роли; env `DRCODE_MAX_CONTEXT_TOKENS` не используется — flat-config
  fallback в 0.5.0 удалён — и в прогоне всё равно вычищается).
- S3: сид — каталог `glossary/` из 18 модулей, brief велит прочитать
  каждый; assertions checks.py: событие «Context compacted», compaction
  start (mid-run pause или turn boundary), `COMPACTION_SUMMARY_PREFIX`
  в `messages`, исходный user-промпт дословно, задача COMPLETED/PASSED,
  pytest зелёный.
- S4: сид — `data/listing.txt` на 25 000 строк, brief велит «проверь
  полный листинг» (run_bash с жирным stdout); assertions checks.py:
  compaction-евент внутри testing-раунда, `tester_messages[-1]` содержит
  summary, вердикт выставлен.
- Источник порога тестера (§1.2, drcode ≥ 0.5.0: конфиг МОДЕЛИ ТЕСТЕРА) —
  объект проверки: `metrics.json` классифицирует его
  (`tester_threshold_from_tester`), отчёт помечает регрессией порог от
  кодинговой модели (допер-ролевое поведение; оговорка про resume-путь
  drcode — в drcode-bench.md §13).
- `metrics.json` также содержит: `repeat_compaction` (повторная компакция
  — деградация после summary) и `compaction_failed`-евенты (в drcode
  failure компакции never fatal: gate отключается, ран продолжается
  несжатым; отчёт помечает это состояние).
- Деградационная combo «слабого компактизатора» — `degradation-weak-compactor`
  в matrix.toml (ручная проверка); полный матричный раннер — этап 5.

Этапы 4–5 плана (§12) наполняют остальные сценарии и матричный раннер.

## S6 — очередь: feature + bug одновременно (этап 5, план §7)

Два brief'а ставятся в очередь ОДНОВРЕМЕННО (feature: `stdev()`, bug:
сломанный `median()`). Assertions checks.py:

- порядок активаций по `activated_at`: баг активируется раньше feature
  (баги сортируются в голову `TaskManager.queued()`);
- гейт «никакой девелопмент, пока идёт testing» (§2/§7): таймстемп
  сообщения кодера не попадает ВНУТРЬ интервала testing-раунда — ни
  своего, ни чужого (интервал-на-интервал давал бы ложные срабатывания:
  транскрипт кодера легитимно покрывает паузы между раундами);
- тот же гейт по логу recorder'а (`model_log.jsonl`, §5): теги ролей
  восстанавливаются сопоставлением записей с ответами транскриптов (та же
  пара токенов), интервалы запросов кодер-тегов и тестер-тегов не
  пересекаются; несопоставленные записи (компактизатор, §1.5) не голосуют
  и не считаются;
- оба brief'а COMPLETED с verification=PASSED, pytest зелёный.

`bench.metrics.analyze_gate` считает тот же гейт для любого прогона
(`gate` в metrics.json, колонка «gate» в отчёте).

## S8 — внутренний fix-loop тестировщика (upstream drcode 18b48f9)

Покрывает путь `set_verification(success=False, retry_here=True)`: сбой
вызван изменениями САМОЙ задачи → `TaskManager.requeue_failed_fix`
возвращает задачу в разработку тому же кодеру (fix_rounds, лимит
`max_dev_rounds` = 3), отчёт тестера становится следующим вводом задачи,
второй круг разработки чинит регрессию, второй testing-раунд ставит
PASSED — без единого вмешательства пользователя.

Отличие от s2a: в s2a соседний тест красен В СИДЕ и падение чужое
(retry_here=False → follow-up пользователя). В S8 полный сид зелёный:
правка кодера (pad() получает обрезку длинных строк) ломает зависимый
test_row ПО ЗАМЫСЛУ — изменение аддитивно относительно собственного
контракта pad() (test_pad закрепляет только короткие строки), поэтому
красным становится ровно один зависимый тест. Бриф объём правки
сознательно ограничивает pad() и велит не трогать остальное, даже если
полный pytest станет красным.

Assertions checks.py: pytest зелёный; задача COMPLETED с
verification=PASSED; событие возврата в разработку дословно
«testing failed — returned for another development round (round 2/3)»
(счётчик инкрементируется ДО составления события, число — номер
ПРЕДСТОЯЩЕГО раунда разработки: бриф — раунд 1, поэтому «2» — единственное
сохранённое доказательство, что fix_rounds дошёл до 1; финальный PASSED
сбрасывает `fix_rounds` в 0); ≥2 testing- и ≥2 development-раунда (отчёт
тестера — ровно один новый prompt в транскрипте кодера); `user_sim.jsonl`
— только запись start, ни одного intervention. Бриф НЕ содержит литерала
«test_row»
(ключа round-2 фикса скриптованного кодера в fake_gateway). Комбо-факторы
не нужны: fix-loop не зависит от контекста/компакции — достаточно
baseline-single-model.

## S9 — research-подсчёт по данным сида (research V1)

Первый research-сценарий: бриф kind=research велит проанализировать
`data/orders.csv` (сид — детерминированный журнал заказов, фиксирован
коммитом) и записать суммарную выручку (sum(amount) по
status="completed") в `docs/report.md` строкой ровно вида
`total: <число>`. Формат закреплён жёстко — от него зависит парсинг.

- research skips the tester (план §7): COMPLETED через mark_done,
  без verification-метки, ноль testing-раундов; `[settle]` без
  `verification` (research + verification="passed" — ошибка загрузки
  сценария), COMPLETED таргета гарантирует базовый settle-критерий.
- Путь вычисления брифом не ограничен (run_bash/python — легитимный
  тул-юз); угадать число нельзя — оно читается из данных.
- Бриф требует создавать отчёт инструментом write_file: правка
  попадает в `task.edited_files`, и обязательный для документных
  заданий `git_commit_docs` её коммитит.

Assertions checks.py (verdict механический): эталон пересчитывается
прямо из сидового CSV (сумма по фильтру) — сид и проверка не разъедутся;
`docs/report.md` существует и содержит ровно одну строку под anchored
regex `^total: (\d+)$`, число совпадает с эталоном; task JSON — ровно
одна задача kind=research, status=completed, ноль testing-раундов,
verification=None; строже — `git log -- docs/report.md` непуст
(git_commit_docs использован; git недоступен → проверка пропускается).
