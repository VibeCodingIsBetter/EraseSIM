import os
import random
import time
import curses

FILENAME = "clear_test.txt"
TIMEOUT = 5      # Оригинальный таймаут между проходами (5 секунд)

# Исторические накопители (влияют на размер тестового файла)
DRIVES = [
    {"name": "⚙️ IBM 350 RAMAC (1956) — Первый в мире HDD", "size": 3750000, "info": "Вес: >1 тонны. 50 дисков по 24\". Общая емкость около 3.75-5 МБ."},
    {"name": "🎛️ Dataram Bulk Core (1976) — Самый первый в мире SSD", "size": 2000000, "info": "Огромный рэковый шкаф за $9,700. 2 Мегабайта на базе RAM/магнитных сердечников."},
    {"name": "⚡ SunDisk Flash SSD (1991) — Первый современный флеш-SSD", "size": 20000000, "info": "20 Мегабайт в формате PCMCIA карты для ноутбуков IBM ThinkPad. Цена: $1,000."},
    {"name": "💾 3.5\" Дискета High-Density (1980-е)", "size": 1474560, "info": "Емкость 1.44 МБ. Легко поддается полному размагничиванию."},
    {"name": "💻 Современный виртуальный сектор (Для быстрых тестов)", "size": 512, "info": "Стандартный блок в 512 байт. Идеален для мгновенной оценки hex-матрицы."}
]

ALGORITHMS = [
    {"name": "💨 БЫСТРОЕ ФОРМАТИРОВАНИЕ (Стирание только оглавления / Данные ЖИВЫ)", "passes": ['quick_format'], "instant": True},
    {"name": "NIST SP 800-88 (1 проход: случайные)", "passes": ['random'], "instant": False},
    {"name": "ГОСТ Р 50739-95 (2 прохода: нули -> случайные)", "passes": ['zeros', 'random'], "instant": False},
    {"name": "DoD 5220.22-M (3 прохода: нули -> единицы -> случайные)", "passes": ['zeros', 'ones', 'random'], "instant": False},
    {"name": "Bruce Schneier (7 проходов: 1 -> 0 -> 5x случайные)", "passes": ['ones', 'zeros'] + ['random']*5, "instant": False},
    {"name": "БЕЗУМНЫЙ МЕТОД: Peter Gutmann (35 проходов!)", "passes": ['random']*4 + ['zeros', 'ones']*12 + ['zeros'] + ['random']*4, "instant": False, "crazy_warn": True},
    {"name": "⚡ СИМУЛЯЦИЯ: Hardware SSD Secure Erase (Мгновенный сброс контроллера)", "passes": ['ones'], "instant": True},
    {"name": "🧲 ДЕГАУССИНГ: Мощный магнитный импульс (Физическое уничтожение)", "passes": ['degauss'], "instant": True}
]

def safe_addstr(stdscr, y, x, text, attr=0):
    try:
        max_y, max_x = stdscr.getmaxyx()
        if y < max_y and x < max_x:
            stdscr.addstr(y, x, text[:max_x - x - 1], attr)
    except curses.error:
        pass

def create_test_file(file_size):
    secrets = [b"TOP_SECRET", b"CONFIDENTIAL", b"PASSWORD_123", b"ENCRYPTED_KEY", b"ACCESS_GRANTED", b"CLEARED_DATA"]
    block_size = 65536  # Оптимизация записи блоками по 64 КБ
    
    block_template = bytearray()
    while len(block_template) < block_size:
        block_template.extend(random.choice(secrets) + f":{random.randint(1000, 9999)}] ".encode('utf-8'))
    block_template = block_template[:block_size]

    written = 0
    with open(FILENAME, "wb") as f:
        while written < file_size:
            to_write = min(block_size, file_size - written)
            f.write(block_template[:to_write])
            written += to_write

def render_hex_matrix(stdscr, start_y, buffer):
    bytes_per_line = 16
    y = start_y
    max_y, _ = stdscr.getmaxyx()
    
    for i in range(0, len(buffer), bytes_per_line):
        if y >= max_y - 4: 
            break
        chunk = buffer[i:i+bytes_per_line]
        hex_string = " ".join(f"{b:02x}" for b in chunk).ljust(47)
        ascii_string = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        
        safe_addstr(stdscr, y, 2, f"{i:04x}:  {hex_string}  | {ascii_string}", curses.color_pair(1))
        y += 1

def run_eraser(stdscr, algo, file_size, selected_drive):
    if not os.path.exists(FILENAME):
        create_test_file(file_size)

    total_passes = len(algo['passes'])
    is_instant = algo.get("instant", False)
    
    # Реалистичный перехват для дегауссинга
    if 'degauss' in algo['passes']:
        max_y, max_x = stdscr.getmaxyx()
        stdscr.clear()
        if max_y > 4 and max_x > 10: stdscr.border()
        
        safe_addstr(stdscr, 1, 2, f" АЛГОРИТМ: {algo['name']} ", curses.color_pair(2))
        safe_addstr(stdscr, 3, 2, "Зарядка конденсаторной батареи дегауссатора...", curses.color_pair(1))
        safe_addstr(stdscr, 4, 2, "Напряжение: [#####---------------] 350V", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.8)
        
        safe_addstr(stdscr, 4, 2, "Напряжение: [#############-------] 700V", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.8)
        
        safe_addstr(stdscr, 4, 2, "Напряжение: [====================] 1200V. ГОТОВ К РАЗРЯДУ.", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(0.6)

        # СКРЫТАЯ ЛОГИКА: Хаотизация магнитных доменов (запись случайного шума)
        try:
            with open(FILENAME, "r+b") as f:
                buf_size = min(65536, file_size)
                f.seek(0)
                written = 0
                while written < file_size:
                    to_write = min(buf_size, file_size - written)
                    pattern = bytearray(random.getrandbits(8) for _ in range(to_write))
                    f.write(pattern)
                    written += to_write
                f.flush()
                os.fsync(f.fileno())  # Принудительно сбрасываем хаос на физический диск
        except Exception:
            pass

        print('\a') # Системный звуковой писк (щелчок разряда)
        stdscr.bkgd(' ', curses.color_pair(2)) # Инвертируем цвета (вспышка)
        stdscr.clear()
        stdscr.refresh()
        time.sleep(0.1) # Короткая вспышка импульса
        
        stdscr.bkgd(' ', curses.color_pair(1)) # Возвращаем нормальный цвет
        stdscr.clear()
        if max_y > 4 and max_x > 10: stdscr.border()
        
        safe_addstr(stdscr, 1, 2, f" АЛГОРИТМ: {algo['name']} ", curses.color_pair(2))
        safe_addstr(stdscr, 3, 2, "ПОДАН ИМПУЛЬС ИНДУКЦИЕЙ 1.5 ТЕСЛА! ⚡⚡⚡", curses.color_pair(2))
        safe_addstr(stdscr, 5, 2, "[КРИТИЧЕСКИЙ СБОЙ ДОМЕНОВ] Магнитная структура plastic разрушена.", curses.color_pair(1))
        safe_addstr(stdscr, 6, 2, "[РАЗРУШЕНИЕ СЕРВОРАЗМЕТКИ] Низкоуровневые треки стерты навсегда.", curses.color_pair(1))
        stdscr.refresh()
        time.sleep(1.5)
        
        if os.path.exists(FILENAME):
            os.remove(FILENAME)
            
        safe_addstr(stdscr, 8, 2, f"[!!!] Накопитель превратился в кирпич. Контроллер потерял позиционирование.", curses.color_pair(1))
        safe_addstr(stdscr, max_y - 2, 2, "Выполнение завершено! Нажмите любую клавишу трусливого возврата...", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()
        return

    # Реалистичный перехват для быстрого форматирования
    if 'quick_format' in algo['passes']:
        max_y, max_x = stdscr.getmaxyx()
        stdscr.clear()
        if max_y > 4 and max_x > 10: stdscr.border()
        
        safe_addstr(stdscr, 1, 2, f" АЛГОРИТМ: {algo['name']} ", curses.color_pair(2))
        
        # Проверяем, включен ли современный виртуальный сектор
        if selected_drive["name"] == "💻 Современный виртуальный сектор (Для быстрых тестов)":
            safe_addstr(stdscr, 3, 2, "[!] Оглавление очищено. ОС запланировала отправку отложенного TRIM...", curses.color_pair(1))
            
            # ЭТАП 1: Затираем только первые 16 байт, как на HDD (TRIM еще не сработал)
            with open(FILENAME, "r+b") as f:
                f.seek(0)
                f.write(b'\x00' * 16) 
                f.flush()
                os.fsync(f.fileno())
                
                f.seek(0)
                preview_data = f.read(64)

            safe_addstr(stdscr, 5, 2, "ОКНО НАБЛЮДЕНИЯ (ДАННЫЕ ВСЁ ЕЩЕ В ЯЧЕЙКАХ — КОНТРОЛЛЕР ЖДЕТ):", curses.A_UNDERLINE | curses.color_pair(1))
            render_hex_matrix(stdscr, 6, preview_data)
            safe_addstr(stdscr, max_y - 4, 2, "[🔥] ВНИМАНИЕ! Прямо сейчас PhotoRec УСПЕЕТ восстановить файлы!", curses.color_pair(2))
            stdscr.refresh()
            
            # ЭТАП 2: Симуляция задержки контроллера (сделаем 10 секунд для демонстрации)
            TRIM_DELAY = 10 
            for t in range(TRIM_DELAY, 0, -1):
                safe_addstr(stdscr, max_y - 3, 2, f"⏳ Буфер контроллера SSD обрабатывает очередь... Очистка через: {t} сек. ", curses.color_pair(1))
                stdscr.refresh()
                time.sleep(1)

            # ЭТАП 3: Отрабатывает отложенный TRIM (полное обнуление)
            stdscr.clear()
            if max_y > 4 and max_x > 10: stdscr.border()
            safe_addstr(stdscr, 1, 2, f" АЛГОРИТМ: {algo['name']} ", curses.color_pair(2))
            safe_addstr(stdscr, 3, 2, "[⚡] ТРИГГЕР: Отработала отложенная команда TRIM (Буфер контроллера сброшен)!", curses.color_pair(1))
            
            with open(FILENAME, "r+b") as f:
                f.seek(0)
                f.write(b'\x00' * file_size)  # Аппаратный сброс ячеек контроллером
                f.flush()
                os.fsync(f.fileno())
                
                f.seek(0)
                preview_data = f.read(64)

            safe_addstr(stdscr, 5, 2, "ОКНО НАБЛЮДЕНИЯ (ОТЛОЖЕННЫЙ TRIM ЗАВЕРШЕН — ДАННЫЕ УНИЧТОЖЕНЫ):", curses.A_UNDERLINE | curses.color_pair(1))
            render_hex_matrix(stdscr, 6, preview_data)
            
            safe_addstr(stdscr, max_y - 4, 2, "[+] Контроллер полностью очистил адреса секторов.", curses.color_pair(1))
            safe_addstr(stdscr, max_y - 3, 2, "[❌] Окно возможностей закрылось. Теперь восстановление невозможно.", curses.color_pair(2))
        
        else:
            # Старая логика для классических дисков без TRIM (данные остаются навсегда)
            safe_addstr(stdscr, 3, 2, "Очистка таблиц разметки (MFT / FAT таблицы)...", curses.color_pair(1))
            stdscr.refresh()
            time.sleep(0.5)

            with open(FILENAME, "r+b") as f:
                f.seek(0)
                f.write(b'\x00' * 16) 
                f.flush()
                os.fsync(f.fileno())

                f.seek(0)
                preview_data = f.read(64)

            safe_addstr(stdscr, 5, 2, "ОКНО НАБЛЮДЕНИЯ (ОГЛАВЛЕНИЕ ЗАДЕТО, НО СЕКРЕТЫ ДАЛЬШЕ ЦЕЛЫ!):", curses.A_UNDERLINE | curses.color_pair(1))
            render_hex_matrix(stdscr, 6, preview_data)
            
            safe_addstr(stdscr, max_y - 4, 2, "[+] Операционная система считает диск ПУСТЫМ и готовым к записи.", curses.color_pair(1))
            safe_addstr(stdscr, max_y - 3, 2, "[🔥] Спецслужбы и PhotoRec достанут отсюда 100% файлов за минуту!", curses.color_pair(2))
            
        safe_addstr(stdscr, max_y - 2, 2, "Выполнение успешно завершено! Нажмите любую клавишу...", curses.color_pair(2))
        stdscr.refresh()
        stdscr.getch()
        return



    with open(FILENAME, "r+b") as f:
        for pass_idx, pass_type in enumerate(algo['passes'], 1):
            max_y, max_x = stdscr.getmaxyx()
            stdscr.clear()
            if max_y > 4 and max_x > 10: stdscr.border()
            
            safe_addstr(stdscr, 1, 2, f" АЛГОРИТМ: {algo['name']} ", curses.color_pair(2))
            
            if is_instant:
                safe_addstr(stdscr, 2, 2, "Подача аппаратного импульса на контроллер... Ячейки сброшены!", curses.color_pair(1))
            else:
                safe_addstr(stdscr, 2, 2, f"Проход {pass_idx} из {total_passes} [{pass_type.upper()}]", curses.color_pair(1))
            
            buf_size = min(65536, file_size)
            if pass_type == 'zeros':
                pattern = b'\x00' * buf_size
            elif pass_type == 'ones':
                pattern = b'\xff' * buf_size
            elif pass_type == 'random':
                pattern = bytearray(random.getrandbits(8) for _ in range(buf_size))

            f.seek(0)
            written = 0
            
            while written < file_size:
                to_write = min(buf_size, file_size - written)
                f.write(pattern[:to_write])
                written += to_write
                
                pct = int((written / file_size) * 100)
                safe_addstr(stdscr, 3, 2, f"Перезапись физических секторов: [{'#' * (pct // 5)}{'-' * (20 - (pct // 5))}] {pct}%", curses.color_pair(1))
                stdscr.refresh()

            f.flush()
            os.fsync(f.fileno())

            f.seek(0)
            preview_data = f.read(64)
            safe_addstr(stdscr, 5, 2, "ОКНО НАБЛЮДЕНИЯ (ПЕРВЫЕ 64 БАЙТА МОДИФИЦИРОВАННОГО СЕКТОРА):", curses.A_UNDERLINE | curses.color_pair(1))
            render_hex_matrix(stdscr, 6, preview_data)
            # ... (конец тела цикла перезаписи прохода внутри run_eraser)
            safe_addstr(stdscr, max_y - 4, 2, "[+] Буфер ОС сброшен на пластины/ячейки через os.fsync().", curses.color_pair(1))
            stdscr.refresh()
            if not is_instant:
                time.sleep(0.1)
                
            if pass_idx < total_passes and not is_instant:
                for t in range(TIMEOUT, 0, -1):
                    if algo.get("crazy_warn", False):
                        safe_addstr(stdscr, max_y - 3, 2, "☕ Сходи попей чай или кофе, вырасти сына, построй дом...", curses.color_pair(2))
                        safe_addstr(stdscr, max_y - 2, 2, f"  ...а мы обо всем позаботимся. До следующего прохода: {t} сек. ", curses.color_pair(1))
                    else:
                        safe_addstr(stdscr, max_y - 2, 2, f"Ожидание следующего прохода алгоритма... {t} сек. ", curses.color_pair(1))
                    stdscr.refresh()
                    time.sleep(1)
            else:
                safe_addstr(stdscr, max_y - 2, 2, "Выполнение успешно завершено! Нажмите любую клавишу...", curses.color_pair(2))
                stdscr.refresh()
                stdscr.getch()


def check_crazy_confirmation(stdscr):
    stdscr.clear()
    stdscr.border()
    safe_addstr(stdscr, 3, 4, "Вы хотите извращаться по полной? (y/n)", curses.color_pair(1))
    stdscr.refresh()
    
    while True:
        key = stdscr.getch()
        if key in [ord('y'), ord('Y'), ord('н'), ord('Н')]:
            return True
        elif key in [ord('n'), ord('N'), ord('т'), ord('Т')]:
            stdscr.clear()
            stdscr.border()
            safe_addstr(stdscr, 5, 4, "Серьезно?", curses.color_pair(2))
            safe_addstr(stdscr, 7, 4, "Нажмите любую клавишу, чтобы трусливо вернуться в меню...", curses.color_pair(1))
            stdscr.refresh()
            stdscr.getch()
            return False


def select_drive_menu(stdscr):
    current_row = 0
    while True:
        max_y, max_x = stdscr.getmaxyx()
        stdscr.clear()
        if max_y < 16 or max_x < 65:
            stdscr.addstr(0, 0, "Растяните окно terminalа шире и выше!")
            stdscr.refresh()
            time.sleep(0.5)
            continue
            
        stdscr.border()
        safe_addstr(stdscr, 1, 2, " === ШАГ 1: ВЫБОР ТИПА НАКОПИТЕЛЯ ДЛЯ СИМУЛЯЦИИ === ", curses.color_pair(2))
        safe_addstr(stdscr, 2, 2, "СТРЕЛКИ - выбор накопителя, ENTER - подтвердить, Q - выход.", curses.color_pair(1))
        safe_addstr(stdscr, 3, 2, "-" * (max_x - 4), curses.color_pair(1))
        
        offset = 5
        for idx, drive in enumerate(DRIVES):
            if idx == current_row:
                safe_addstr(stdscr, offset + idx, 4, f"> {drive['name']} ({drive['size'] / 1000000:.2f} МБ)", curses.color_pair(2))
            else:
                safe_addstr(stdscr, offset + idx, 4, f"  {drive['name']} ({drive['size'] / 1000000:.2f} МБ)", curses.color_pair(1))
                
        safe_addstr(stdscr, offset + len(DRIVES) + 2, 4, "ИСТОРИЧЕСКАЯ СПРАВКА ПО ЖЕЛЕЗУ:", curses.A_UNDERLINE | curses.color_pair(1))
        safe_addstr(stdscr, offset + len(DRIVES) + 3, 4, DRIVES[current_row]["info"], curses.color_pair(1))
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == curses.KEY_UP: 
            current_row = (current_row - 1) % len(DRIVES)
        elif key == curses.KEY_DOWN: 
            current_row = (current_row + 1) % len(DRIVES)
        elif key in [curses.KEY_ENTER, 10, 13]: 
            return DRIVES[current_row]
        elif key in [ord('q'), ord('Q'), ord('й'), ord('Й')]: 
            return None


def menu_loop(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.curs_set(0)
    stdscr.keypad(True)
    
    while True:
        selected_drive = select_drive_menu(stdscr)
        if not selected_drive:
            break
            
        file_size = selected_drive["size"]
        create_test_file(file_size)
        current_algo_row = 0
        
        while True:
            max_y, max_x = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.border()
            stdscr.bkgd(' ', curses.color_pair(1))
            
            safe_addstr(stdscr, 1, 2, f" === ШАГ 2: ВЫБОР АЛГОРИТМА ОЧИСТКИ ({selected_drive['name']}) === ", curses.color_pair(2))
            safe_addstr(stdscr, 2, 2, "ENTER - запустить затирание, ESC/B - вернуться к выбору диска.", curses.color_pair(1))
            safe_addstr(stdscr, 3, 2, "-" * (max_x - 4), curses.color_pair(1))
            
            offset = 4
            for idx, algo in enumerate(ALGORITHMS):
                if idx == current_algo_row:
                    safe_addstr(stdscr, offset + idx, 4, f"> {algo['name']}", curses.color_pair(2))
                else:
                    safe_addstr(stdscr, offset + idx, 4, f"  {algo['name']}", curses.color_pair(1))
                    
            restore_idx = len(ALGORITHMS)
            if current_algo_row == restore_idx:
                safe_addstr(stdscr, offset + restore_idx, 4, "> [Пересоздать тестовый файл / Сбросить к секретам]", curses.color_pair(2))
            else:
                safe_addstr(stdscr, offset + restore_idx, 4, "  [Пересоздать тестовый файл / Сбросить к секретам]", curses.color_pair(1))
                
            preview_y = offset + restore_idx + 2
            if preview_y + 5 < max_y:
                safe_addstr(stdscr, preview_y, 2, "ТЕКУЩЕЕ СОСТОЯНИЕ НАЧАЛЬНЫХ СЕКТОРОВ НА СИМУЛИРУЕМОМ ДИСКЕ:", curses.A_UNDERLINE | curses.color_pair(1))
                if os.path.exists(FILENAME):
                    try:
                        with open(FILENAME, "rb") as f:
                            current_data = f.read(64)
                        render_hex_matrix(stdscr, preview_y + 1, current_data)
                    except Exception:
                        safe_addstr(stdscr, preview_y + 1, 2, "Ошибка чтения секторов...", curses.color_pair(1))
                else:
                    safe_addstr(stdscr, preview_y + 1, 2, "Диск полностью чист/размагничен! Выберите [Пересоздать файл].", curses.color_pair(2))
                    
            stdscr.refresh()
            key = stdscr.getch()
            
            # Единый блок ветвления для нажатых клавиш
            if key == curses.KEY_UP:
                current_algo_row = (current_algo_row - 1) % (restore_idx + 1)
            elif key == curses.KEY_DOWN:
                current_algo_row = (current_algo_row + 1) % (restore_idx + 1)
            elif key in [27, ord('b'), ord('B'), ord('и'), ord('И')]:
                break
            elif key in [curses.KEY_ENTER, 10, 13]:
                if current_algo_row < len(ALGORITHMS):
                    algo = ALGORITHMS[current_algo_row]
                    drive_name = selected_drive["name"]

                    # ИСТОРИЧЕСКИЙ ФИЛЬТР 1: Secure Erase
                    if "Secure Erase" in algo["name"] and ("IBM 350" in drive_name or "Дискета" in drive_name):
                        stdscr.clear()
                        stdscr.border()
                        safe_addstr(stdscr, 3, 4, "❌ ОШИБКА СОВМЕСТИМОСТИ ЖЕЛЕЗА", curses.color_pair(2))
                        safe_addstr(stdscr, 5, 4, f"Накопитель: {drive_name}", curses.color_pair(1))
                        safe_addstr(stdscr, 6, 4, "Аппаратный Secure Erase невозможен! У этого носителя", curses.color_pair(1))
                        safe_addstr(stdscr, 7, 4, "просто нет современного контроллера для выполнения этой команды.", curses.color_pair(1))
                        safe_addstr(stdscr, 9, 4, "Нажмите любую клавишу для возврата...", curses.color_pair(2))
                        stdscr.refresh()
                        stdscr.getch()
                        continue

                    # ИСТОРИЧЕСКИЙ ФИЛЬТР 2: Дегауссинг
                    if "ДЕГАУССИНГ" in algo["name"] and ("IBM 350" in drive_name or "Dataram Bulk Core" in drive_name):
                        stdscr.clear()
                        stdscr.border()
                        safe_addstr(stdscr, 3, 4, "❌ ОШИБКА ФИЗИЧЕСКОЙ СОВМЕСТИМОСТИ", curses.color_pair(2))
                        safe_addstr(stdscr, 5, 4, f"Накопитель: {drive_name}", curses.color_pair(1))
                        
                        if "IBM 350" in drive_name:
                            safe_addstr(stdscr, 6, 4, "Дегауссинг физически невозможен! Этот гигант весит 1 тонну", curses.color_pair(1))
                            safe_addstr(stdscr, 7, 4, "и имеет размер с два холодильника. Вы не сможете засунуть", curses.color_pair(1))
                            safe_addstr(stdscr, 8, 4, "целый шкаф с 24-дюймовыми блинами в лабораторный дегауссатор.", curses.color_pair(1))
                        else:
                            safe_addstr(stdscr, 6, 4, "Дегауссинг физически невозможен! Монолитное стальное шасси", curses.color_pair(1))
                            safe_addstr(stdscr, 7, 4, "размером 19x15.75 дюймов весит слишком много и спроектировано", curses.color_pair(1))
                            safe_addstr(stdscr, 8, 4, "под серверную стойку. Корпус просто не влезет в дегауссатор.", curses.color_pair(1))
                            safe_addstr(stdscr, 10, 4, "💡 К тому же это RAM на магнитных сердечниках — для очистки", curses.color_pair(2))
                            safe_addstr(stdscr, 11, 4, "   достаточно просто обесточить ОЗУ.", curses.color_pair(1))
                            
                        safe_addstr(stdscr, max_y - 2, 4, "Нажмите любую клавишу для возврата...", curses.color_pair(2))
                        stdscr.refresh()
                        stdscr.getch()
                        continue


                    # Проверка на безумный метод Гутмана
                    if algo.get("crazy_warn", False):
                        if not check_crazy_confirmation(stdscr): 
                            continue

                    run_eraser(stdscr, algo, file_size, selected_drive)

                elif current_algo_row == restore_idx:
                    create_test_file(file_size)
                    
        if os.path.exists(FILENAME):
            os.remove(FILENAME)



def main():
    curses.wrapper(menu_loop)
    print("\n[+] Симуляция успешно завершена. Все временные файлы удалены.")


if __name__ == "__main__":
    main()
