from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:0.3f} ч.; '
                    'Дистанция: {distance:0.3f} км; '
                    'Ср. скорость: {speed:0.3f} км/ч; '
                    'Потрачено ккал: {calories:0.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    COEFF_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = self.get_distance() / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Вид тренировки не определен.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.COEFF_CALORIE_1
                                * self.get_mean_speed()
                                - self.COEFF_CALORIE_2)
                               * self.weight
                               / self.M_IN_KM
                               * self.duration
                               * self.COEFF_MIN)
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    COEFF_SQRT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.COEFF_CALORIE_1
                                * self.weight
                                + (self.get_mean_speed() ** self.COEFF_SQRT
                                   // self.height)
                                * self.COEFF_CALORIE_2
                                * self.weight)
                               * self.duration
                               * self.COEFF_MIN)
        return self.spent_calories

    def __str__(self):
        return f'{self}'


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = (self.length_pool
                           * self.count_pool
                           / self.M_IN_KM
                           / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.get_mean_speed()
                                + self.COEFF_CALORIE_1)
                               * self.COEFF_CALORIE_2
                               * self.weight)
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in package:
        raise ValueError(f'Неправильный тип тренировки. '
                         f'Доступные ключи: {list(package.keys())}')
    return package[workout_type](* data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
