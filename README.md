## Запуск проекта

## Docker

Для создания образа и одновременного запуская контейнера с IDE запустите:
```commandline
sudo docker compose up --build
```

Для того чтобы запустить контейнер по созданному образу, используйте:
```commandline
sudo docker compose up
```

### Linux

Установите файлы CocoR, виртуальное окружение и все необходимые библиотеки с помощью: 
```commandline
build/setup.sh
```

После этого запустите основную программу:
```commandline
python3 src/GUI/main.py 
```

### Windows

Установите файлы CocoR, виртуальное окружение и все необходимые библиотеки с помощью: 
```commandline
build/setup.bat
```
После этого запустите основную программу в файле: 
```
src/GUI/main.py
``` 