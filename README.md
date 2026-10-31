# 🧲 Data Destruction Simulator (TUI) / Симулятор уничтожения данных

An interactive TUI simulator that visualizes how various data sanitization and destruction algorithms overwrite storage media.
Интерактивный симулятор с текстовым интерфейсом TUI, который наглядно визуализирует работу различных алгоритмов затирания и уничтожения данных на носителях.

---

## 🌍 Language / Язык
* [English](#english)
* [Русский](#русский)

---

## English

This project is an educational simulation tool built with Python and `curses`. It demonstrates how computer forensics and data sanitization standards modify physical disk sectors by displaying a live hex matrix view during the erasure process.

### ✨ Features
* **Historical Hardware Profiles:** Simulate data destruction on classic and modern drives (from the 1956 IBM 350 RAMAC to modern SSD virtual sectors).
* **Industry Standards:** Experience 7 different destruction methods including NIST SP 800-88, DoD 5220.22-M, GOST R 50739-95, and the legendary 35-pass Peter Gutmann algorithm.
* **Live Hex Matrix View:** Watch "secret data" strings (`TOP_SECRET`, `PASSWORD_123`) turn into zeros, ones, or random noise in real-time.
* **Advanced Animations:** Immersive special effects for hardware-level operations like **SSD Secure Erase** and **Degaussing** (complete with screen flashes and audio alerts).
* **100% Safe:** All operations are performed strictly inside a temporary mock file (`clear_test.txt`). Your files are completely safe.

### 🚀 How to Run

#### 1. Prerequisites
* **Linux / macOS:** Python 3.x (the `curses` library is built-in).
* **Windows:** You need to install the Windows adaptation of the `curses` library. Open your terminal/command prompt and run:
  ```bash
  pip install windows-curses
  ```

#### 2. Execution
Clone the repository and run the script:
```bash
python main.py
```
*Replace `main.py` with the actual name of your script file.*

### 📄 License
This project is licensed under the MIT License - feel free to use, modify, and share!

---

## Русский

Этот проект представляет собой обучающий симулятор, разработанный на Python с использованием библиотеки `curses`. Он демонстрирует, как криминалистические стандарты и протоколы очистки данных модифицируют физические секторы диска, отображая живую hex-матрицу в процессе затирания.

### ✨ Особенности
* **Профили исторического железа:** Симуляция уничтожения данных на легендарных накопителях (от IBM 350 RAMAC 1956 года до современного виртуального сектора).
* **Мировые стандарты ИБ:** 7 встроенных методов очистки, включая DoD 5220.22-M, ГОСТ Р 50739-95 и 35-проходный метод Питера Гутмана.
* **Окно наблюдения (Hex-матрица):** Наблюдайте в реальном времени, как строки «секретных данных» превращаются в нули, единицы или случайный шум.
* **Интерактивные анимации:** Спецэффекты для аппаратных операций, таких как **SSD Secure Erase** и **Дегауссинг** (с мерцанием экрана и звуковым щелчком разряда).
* **Абсолютная безопасность:** Все операции происходят строго внутри одного временного тестового файла (`clear_test.txt`). Скрипт физически не может сломать ваши файлы.

### 🚀 Как запустить

#### 1. Подготовка
* **Linux / mac:** Нужен только Python 3.x (библиотека `curses` уже встроена в ОС).

* **Windows:** Стандартный `curses` не поддерживается Windows из коробки. Перед запуском установите адаптацию библиотеки, выполнив в терминале/командной строке:
  
  pip install windows-curses
  ```

#### 2. Запуск
Склонируйте репозиторий и запустите скрипт:
```bash
python main.py
```
*Замените `main.py` на имя вашего файла со скриптом.*

### 📄 Лицензия
Этот проект распространяется под лицензией MIT — вы можете свободно использовать, изменять и делиться им!
