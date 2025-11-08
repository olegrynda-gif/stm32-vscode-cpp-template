#include "app.hpp"
#include "stm32f1xx_hal.h"
#include "gpio.h"

void App::init()
{
    // Тут здійснюється ініціалізація, наприклад GPIO
}

void App::run()
{
    HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
    HAL_Delay(100);
}
