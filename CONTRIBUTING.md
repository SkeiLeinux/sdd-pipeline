# Contributing

Everything here is public domain: fork it, change it, ship it, no permission needed. Changes back are welcome.

- **Skills and subagent instructions** are code. A pull request says which agent failure it fixes or which step it adds. Edit `.agents/`, then run `python tools/sync_agents.py`.
- **Checker rules** go into `tools/check.py` with a rule code in the message and a test in `tools/tests/` that breaks the example and expects the code.
- **Templates**: a new `## ` heading becomes a required section of every unit of that type - update the example in `examples/` in the same change.
- **Before a pull request**: `python -m unittest discover -s tools/tests` and `python tools/check.py` without errors.
- **Examples** use invented organizations and synthetic data only.

---

Все здесь - общественное достояние: форкайте, меняйте, используйте без разрешения. Улучшения обратно приветствуются. Правила те же: скиллы - через `.agents/` и `sync_agents.py`, новое правило проверки - с тестом, новый заголовок шаблона - вместе с правкой примера, перед pull request - тесты и `check.py` без ошибок, в примерах - только вымышленные данные.
