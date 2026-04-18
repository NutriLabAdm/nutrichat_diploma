# UML Converter Tools

Набор скриптов для генерации диаграмм из различных форматов.

## Требования

```bash
pip install pillow plantuml requests
```

## Quick Start

```bash
# SVG → PNG
python svg2png_converter.py input.svg output.png

# PlantUML → PNG
python plantuml_converter.py input.puml output.png
```

## Использование

### 0. SVG → PNG (Pillow)

```bash
python svg2png_converter.py input.svg output.png
python svg2png_converter.py input.svg --scale=2
```

**Ограничения:** Базовая поддержка (rect, line, text). Для сложных SVG используйте Inkscape или онлайн-конвертеры.

### 1. PlantUML → SVG/PNG (онлайн-сервер)

```bash
python plantuml_converter.py input.puml output.svg
python plantuml_converter.py input.puml output.png
```

**Примечание:** Использует публичный сервер plantuml.com. Для надёжной работы скачайте [PlantUML](https://plantuml.com/download) локально.

### 2. Mermaid → SVG (mmdc)

```bash
mmdc -i input.mmd -o output.svg -w 1200
```

### 3. Локальный PlantUML (рекомендуется)

1. Скачайте `plantuml.jar` с https://plantuml.com/download
2. Запустите:
```bash
java -jar plantuml.jar -tsvg input.puml
java -tpng input.puml
```

## Примеры

```bash
# Mermaid
mmdc -i diagram.mmd -o diagram.svg -w 1200 -b white

# PlantUML локально
java -jar plantuml.jar -tsvg -o ./output input.puml
```

## Troubleshooting

### Ошибка "Connection refused"
- Проверьте интернет-соединение
- Используйте локальный PlantUML

### Ошибка "cairo library not found"
- Установите cairo для вашей ОС
- Или используйте mmdc для Mermaid диаграмм