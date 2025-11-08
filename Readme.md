1. Що потрібно встановити
🔹 Основні компоненти:

Visual Studio Code
→ https://code.visualstudio.com/

ARM GCC Toolchain
→ GNU Arm Embedded Toolchain (arm-none-eabi-gcc)

(додай до PATH, щоб arm-none-eabi-gcc --version працював у терміналі)

STM32CubeMX (генератор ініціалізації проєктів)
→ https://www.st.com/en/development-tools/stm32cubemx.html

STM32CubeProgrammer (для прошивки через ST-Link, DFU, UART)
→ https://www.st.com/en/development-tools/stm32cubeprog.html

ST-LINK драйвери
→ https://www.st.com/en/development-tools/stsw-link009.html

🧩 2. Додатки (Extensions) для VS Code
Extension	Призначення
Cortex-Debug	Налагодження STM32 через ST-Link, J-Link, OpenOCD
C/C++ (Microsoft)	IntelliSense, автодоповнення, навігація
CMake Tools	Якщо використовуєш CMake для збірки
Makefile Tools	Якщо проект на Makefile (CubeMX)
Arm Assembly (опціонально)	Подсвітка асемблера
PlatformIO IDE (альтернатива)	Повноцінне середовище для STM32 з інтегрованим toolchain

Створи проект у CubeMX:
Обери MCU (наприклад, STM32F103C8T6);
Налаштуй тактування, пінмап, UART, SPI тощо;
У Project Manager → Toolchain / IDE вибери Makefile;
Згенеруй проект.

Відкрий папку у VS Code.
Ти побачиш Makefile, Core/, Drivers/ та інші каталоги.
Створи файл c_cpp_properties.json у .vscode:
{
  "configurations": [
    {
      "name": "STM32",
      "includePath": [
        "${workspaceFolder}/Core/Inc",
        "${workspaceFolder}/Drivers/STM32F1xx_HAL_Driver/Inc",
        "${workspaceFolder}/Drivers/CMSIS/Device/ST/STM32F1xx/Include",
        "${workspaceFolder}/Drivers/CMSIS/Include"
      ],
      "defines": [
        "USE_HAL_DRIVER",
        "STM32F103xB"
      ],
      "compilerPath": "C:/Program Files/Arm GNU Toolchain/bin/arm-none-eabi-gcc.exe",
      "cStandard": "c11",
      "cppStandard": "c++17",
      "intelliSenseMode": "gcc-arm"
    }
  ],
  "version": 4
}

Створи launch.json для налагодження (Cortex-Debug):
{
  "configurations": [
    {
      "name": "Debug STM32",
      "type": "cortex-debug",
      "request": "launch",
      "servertype": "stlink",
      "cwd": "${workspaceFolder}",
      "executable": "${workspaceFolder}/build/firmware.elf",
      "device": "STM32F103C8",
      "runToEntryPoint": "main",
      "svdFile": "${workspaceFolder}/STM32F103.svd"
    }
  ]
}

Додати потрібні шляхи до toolchain
Для поточного користувача:
$old = [Environment]::GetEnvironmentVariable("Path", "User")
$new = $old + ";C:\MyTools\bin"
[Environment]::SetEnvironmentVariable("Path", $new, "User")

Для всієї системи (адмін-права):
$old = [Environment]::GetEnvironmentVariable("Path", "Machine")
$new = $old + ";C:\MyTools\bin"
[Environment]::SetEnvironmentVariable("Path", $new, "Machine")

Перевірка
Після додавання шляху перевір:
echo %PATH%
або в PowerShell:
$env:PATH
І переконайся, що твій шлях присутній.

Установити GNU Make через MSYS2 (рекомендовано)
Завантаж MSYS2 → https://www.msys2.org
Встанови й відкрий MSYS2 MINGW64 термінал
Виконай:
pacman -S make
Знайди шлях до make.exe:
C:\msys64\usr\bin\make.exe
Додай цей шлях у PATH (як ми робили раніше через sysdm.cpl або setx /M PATH).
Перезапусти VS Code →
у терміналі виконай:
make --version

✅ Якщо бачиш GNU Make 4.x, усе працює.

Використати OpenOCD як GDB-сервер
Якщо не хочеш ставити ще один ST-інсталятор:
Встанови OpenOCD (через MSYS2 або окремо):

pacman -S openocd

Вкажи у launch.json:
"servertype": "openocd",
"serverpath": "C:/msys64/usr/bin/openocd.exe",
"configFiles": [
    "interface/stlink.cfg",
    "target/stm32f1x.cfg"
],


(файли конфігурації є в папці OpenOCD share/openocd/scripts).

Після запуску VS Code у вікні TERMINAL → Cortex-Debug (gdb-server) має з’явитися:

Info : STLINK V2J39S7 (API v2) VID:PID 0483:374B
Info : stm32f1x.cpu: hardware has 6 breakpoints, 4 watchpoints

Щоб встановити **Python** у Windows 11, виконайте такі кроки:

### 1. Завантаження інсталятора

1. Відкрийте браузер і перейдіть на офіційний сайт Python:
   [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Натисніть кнопку **"Download Python 3.x.x"** (рекомендована версія для Windows).

### 2. Запуск інсталятора

1. Запустіть завантажений `.exe` файл.
2. **Обов’язково поставте галочку** біля пункту **"Add Python to PATH"** (додає Python до змінної середовища, щоб ви могли викликати його з командного рядка).
3. Натисніть **"Install Now"**.

### 3. Перевірка встановлення

1. Відкрийте **Command Prompt** або PowerShell (Win + R → `cmd` або `powershell` → Enter).
2. Введіть:

   ```sh
   python --version
   ```

   або:

   ```sh
   py --version
   ```

   Якщо все встановлено правильно – ви побачите версію Python.

### 4. Встановлення pip (якщо потрібно)

Зазвичай pip встановлюється автоматично разом із Python. Перевірте:

```sh
pip --version
```

### 5. (Необов’язково) Встановлення IDE або редактора коду

* **VS Code** – популярний безкоштовний редактор: [https://code.visualstudio.com/](https://code.visualstudio.com/)
* Можна також використовувати PyCharm, Sublime Text, Notepad++ тощо.

Готово — тепер Python встановлено і готовий до використання 🚀
Якщо виникнуть проблеми — запитуйте!
