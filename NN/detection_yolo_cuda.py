from ultralytics import YOLO
from pathlib import Path
from PIL import Image

# Загрузка более мощной модели YOLOv8 (например, Extra Large)
model = YOLO('yolov8x.pt').to('cuda')  # Перенос модели на GPU

# Путь к папке с изображениями
photo_dir = Path("photos")
output_dir = Path("detections")
output_dir.mkdir(exist_ok=True)

# Обрабатываем изображения
for photo_path in photo_dir.glob("*.*"):
    if photo_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:  # Поддерживаемые форматы
        print(f"Обрабатывается: {photo_path}")

        # Выполнение детекции
        results = model(photo_path)

        # Сохранение аннотированных изображений
        for i, result in enumerate(results):
            output_file = output_dir / f"{photo_path.stem}_result_{i}.jpg"
            annotated_img = result.plot()  # Аннотированное изображение (numpy array)
            Image.fromarray(annotated_img).save(output_file)  # Сохраняем как JPG
            print(f"Результат сохранён: {output_file}")

print(f"Обработка завершена. Результаты сохранены в папке: {output_dir}")
