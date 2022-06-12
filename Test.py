class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

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
        self.mean_speed = self.distance / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self):
        """Вернуть информационное сообщение о выполненной тренировке."""
        print(self.get_distance()),
        print(self.get_mean_speed()),
        print(self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    coeff_min: int = 60

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.coeff_calorie_1
                                * self.mean_speed
                                - self.coeff_calorie_2)
                               * self.weight
                               / self.M_IN_KM
                               * self.duration
                               * self.coeff_min)
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029
    coeff_min: int = 60
    coeff_sqrt: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.coeff_calorie_1
                                * self.weight
                                + (self.mean_speed ** self.coeff_sqrt // self.height)
                                * self.coeff_calorie_2
                                * self.weight)
                               * self.duration
                               * self.coeff_min)
        return self.spent_calories

    def __str__(self):
        return f'{self}'

class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2

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
        self.spent_calories = ((self.mean_speed
                                + self.coeff_calorie_1)
                               * self.coeff_calorie_2
                               * self.weight)
        return self.spent_calories

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    package = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    try:
        return package[workout_type](* data)
    except KeyError:
        print('Такой тренировки не существует')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)