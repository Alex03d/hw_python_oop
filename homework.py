from dataclasses import dataclass


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        message = f' Тип тренировки: {self.training_type};' \
                  f' Длительность: {self.duration} ч.;' \
                  f' Дистанция: {self.distance} км;' \
                  f' Ср.скорость: {self.speed} км/ч;' \
                  f' Потрачено ккал: {self.calories}.'
        return print(message)


@dataclass
class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65

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

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(self,
                                    self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories()
                                    )
        return training_info


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        spent_calories = ((coeff_calorie_1 * self.mean_speed
                           - coeff_calorie_2) * self.weight
                          / self.M_IN_KM * self.duration * 60)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        spent_calories = ((coeff_calorie_1 * self.weight
                           + (self.mean_speed ** 2 // self.height)
                           * coeff_calorie_2
                           * self.weight) * self.duration * 60)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        self.mean_speed = (self.length_pool
                           * self.count_pool
                           / self.M_IN_KM / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_1 = 2
        spent_calories = ((self.mean_speed
                           + coeff_calorie_1) * coeff_calorie_1
                          * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    package = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    return package[workout_type], (*data)


def main(training: Training) -> None:
    """Главная функция."""
    i = training
    if i[0] == Swimming:
        ii = Swimming(i[1], i[2], i[3], i[4], i[5])
        iii = ii.show_training_info()
        iii.get_message()
    elif i[0] == Running:
        ii = Running(i[1], i[2], i[3])
        iii = ii.show_training_info()
        iii.get_message()
    elif i[0] == SportsWalking:
        ii = SportsWalking(i[1], i[2], i[3], i[4])
        iii = ii.show_training_info()
        iii.get_message()
    else:
        print('Error')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
