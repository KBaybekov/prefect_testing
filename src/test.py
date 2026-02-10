#from dotenv import load_dotenv
from prefect import task, flow
from prefect.tasks import task_input_hash
from datetime import timedelta
import time 


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=5))
def process_data(x: int, y: int) -> int:
    """Простая задача для обработки данных"""
    print(f"Обрабатываю данные: {x} и {y}")
    print()
    time.sleep(45)  # Имитация долгой операции
    result = x * y
    print(f"Результат обработки: {result}")
    return result

@task
def validate_result(value: int) -> bool:
    """Задача для валидации результата"""
    print(f"Проверяю результат: {value}")
    is_valid = value > 0
    print(f"Результат валиден: {is_valid}")
    return is_valid

@task
def save_result(value: int, is_valid: bool) -> str:
    """Задача для сохранения результата"""
    if is_valid:
        message = f"Сохранено значение: {value}"
    else:
        message = f"Ошибка: значение {value} невалидно"
    print(message)
    return message


@flow(name="test-pipeline", log_prints=True)
def test_pipeline(x: int = 5, y: int = 3):
    """Основной пайплайн"""
    print("Запуск тестового пайплайна...")
    
    # Выполнение задач
    processed_data = process_data(x, y)
    validation = validate_result(processed_data)
    result_message = save_result(processed_data, validation)
    
    print("Пайплайн завершен!")
    return result_message

if __name__ == "__main__":
    # Запуск пайплайна
    result = test_pipeline(5, 16)
    print(f"Финальный результат: {result}")