---
index: 1
module: module_5
task: encoder
previous: electric_motor
next: odometer
---
# Урок 1: Энкодер

## Цель урока
Изучить энкодеры и их назначение в движении робота.

## Введение
В предыдущих уроках мы управляли движением робота, включая моторы на определенное время. Однако этот метод не очень точный, так как моторы могут работать по-разному в зависимости от уровня заряда батареи, типа поверхностей и механических особенностей. Чтобы сделать движение робота более точным, нам нужно измерять, насколько на самом деле поворачивается каждое колесо. Для этого используются энкодеры!

## Теория

### Что такое энкодер?

Энкодер - это датчик, измеряющий вращение. В робототехнике обычно используются "ротационные энкодеры" - устройства, отслеживающие, насколько повернулся вал электродвигателя. Существует два основных типа:

1. **Абсолютные энкодеры**: Показывают точное положение при вращении (как компас, показывающий север)
2. **Инкрементальные энкодеры**: Выдает за один оборот определенное количество импульсов.


### Получение значений энкодера в нашем роботе

В этом уроке мы будем измерять вращение колес робота в градусах, где:
- Полный оборот колеса вперед = +360°
- Полный оборот колеса назад = -360°
Каждое колесо имеет свой энкодер, поэтому мы будем измерять вращение каждого колеса отдельно. Левый энкодер для левого колеса, а правый энкодер для правого колеса.

Вы сможете использовать следующие функции:
```cpp
robot.encoderDegreesLeft()   // Get left wheel rotation in degrees
robot.encoderDegreesRight()  // Get right wheel rotation in degrees
robot.resetLeftEncoder()     // Reset left encoder to 0
robot.resetRightEncoder()    // Reset right encoder to 0
```

### Расстояние и вращение

Для колеса диаметром D один полный оборот равен расстоянию π * D. У колес нашего робота диаметр 3.5 см, поэтому:
- Один полный оборот = 3.5 * π ≈ 11 см

Эта зависимость помогает нам преобразовывать градусы вращения в фактически пройденное расстояние.

## Задание
Допишите программу так, чтобы демонстрировались значения энкодеров на разных этапах движения робота:
1. Движение робота вперед на один оборот колеса.
2. Движение робота назад на один оборот колеса.
3. Выведите значения энкодера в трех точках:
   - Начальная позиция.
   - Значение после движения вперед
   - Значение после движения назад

Используйте новые функции для получения значений энкодера для левого и правого колес соответственно. Выведите эти значения и сравните их на разных этапах движения робота.
```cpp
#include <lineRobot.h>
void setup() {
    // Reset encoders values
    robot.resetLeftEncoder();
    robot.resetRightEncoder();
    // Read start position values
  printMQTT("START POSITION");
    printMQTT("LEFT:");
    // Will take encoder values in degrees
    // Assume one rotation ~360°
    // printMQTT(robot.encoderDegreesLeft()); // TODO: this line should be done by student
    printMQTT("RIGHT:");
    //printMQTT(robot.encoderDegreesRight()); // TODO: this line should be done by student
    
    // Move forward
    robot.moveForwardDistance(3.5 * 2 * 3.14159);  // one rotation forward (wheels diameter * pi)
    printMQTT("FORWARD MOVEMENT POSITION");
    printMQTT("LEFT:");
    //printMQTT(robot.encoderDegreesLeft()); // TODO: this line should be done by student
    printMQTT("RIGHT:");
    //printMQTT(robot.encoderDegreesRight()); // TODO: this line should be done by student
    
    delay(500);
    
    // Move backward
    robot.moveBackwardDistance(3.5 * 2 * 3.14159);  // one rotation backward (wheels diameter * pi)
    printMQTT("BACKWARD MOVEMENT POSITION");
    printMQTT("LEFT:");
   // printMQTT(robot.encoderDegreesLeft()); //TODO: this line should be done by student
    printMQTT("RIGHT:");
    //printMQTT(robot.encoderDegreesRight()); //TODO: this line should be done by student
}

void loop() {
    delay(1000);
}
```

## Заключение
Вы изучили энкодеры - датчики для измерения движений робота. Понимание того, как они работают и как считывать их значения нужно для продвинутого управления роботом. В следующем уроке мы используем энкодеры для создания одометра, который будет подсчитывать пройденное роботом расстояние!