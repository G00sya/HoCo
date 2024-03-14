# Проект по созданию языка программирования для умного дома

#  Окружение

Установка окружения

```bash
pip install -r requirements.txt
```

Установка гит хуков
```bash
pip install pre-commit
pre-commit install --install-hooks
```

Ручной запуск хуков
```bash
pre-commit run --show-diff-on-failure --color=always --all-files
```

Обновление пакетов в окружении
```bash
pip install pip-tools
pip-sync requirements.txt
```
