#include "app_c.h"
#include "app.hpp"

static App appInstance;

extern "C" void *app_init_c()
{
    // return static_cast<void *>(new App());
    appInstance.init();                       // Викликаємо метод ініціалізації
    return static_cast<void *>(&appInstance); // Повертаємо вказівник на екземпляр
}

extern "C" void app_run_c(void *app)
{
    static_cast<App *>(app)->run();
}
