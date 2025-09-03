import time
import gpiod

# Настройка пина реле (GPIO23)
RELAY_PIN = 23

# Инициализируем переменные
chip = None
line = None

try:
    # Получаем доступ к GPIO чипу
    chip = gpiod.Chip('gpiochip4')  # На Raspberry Pi 5 обычно gpiochip4
    print("Чип GPIO успешно открыт")
    
    # Запрашиваем линию GPIO для управления
    line = chip.get_line(RELAY_PIN)
    print(f"Линия GPIO {RELAY_PIN} получена")
    
    # Настраиваем линию как выход
    line.request(consumer="relay_control", type=gpiod.LINE_REQ_DIR_OUT)
    print("Линия настроена как выход")
    
    # Включаем реле (устанавливаем высокий уровень)
    line.set_value(1)
    print("Устройство включено на 10 секунд")
    
    # Ждем 10 секунд
    time.sleep(10)
    
    # Выключаем реле (устанавливаем низкий уровень)
    line.set_value(0)
    print("Устройство выключено")

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")

finally:
    # Всегда освобождаем ресурсы
    print("Запуск процедуры очистки...")
    
    # Гарантированно выключаем реле
    if line:
        try:
            line.set_value(0)
            print("Реле гарантированно выключено")
        except Exception as e:
            print(f"Ошибка при выключении реле: {str(e)}")
    
    # Освобождаем линию
    if line:
        try:
            line.release()
            print("Линия GPIO освобождена")
        except Exception as e:
            print(f"Ошибка при освобождении линии: {str(e)}")
    
    # Закрываем чип
    if chip:
        try:
            chip.close()
            print("Чип GPIO закрыт")
        except Exception as e:
            print(f"Ошибка при закрытии чипа: {str(e)}")
    
    print("Процедура очистки завершена")