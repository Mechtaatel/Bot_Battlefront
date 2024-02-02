"""
Авторские права (c) 2009 г. Райан Киркман

Разрешение настоящим предоставляется бесплатно любому лицу
получение копии этого программного обеспечения и соответствующей документации
файлы («Программное обеспечение») для работы с Программным обеспечением без
ограничение, включая, помимо прочего, права на использование,
копировать, изменять, объединять, публиковать, распространять,
сублицензировать и/или продавать
копий Программного обеспечения и разрешать лицам, которым
Для этого предоставляется программное обеспечение при условии 
соблюдения следующих условий:
условия:

Вышеупомянутое уведомление об авторских правах и настоящее уведомление о разрешении должны быть
включены во все копии или существенные части Программного обеспечения.

ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ,
ЯВНЫЕ ИЛИ ПОДРАЗУМЕВАЕМЫЕ, ВКЛЮЧАЯ, НО НЕ ОГРАНИЧИВАЯСЬ, ГАРАНТИИ
ТОРГОВОЙ ПРИГОДНОСТИ, ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННОЙ ЦЕЛИ И
НЕНАРУШЕНИЕ ПРАВ. НИ ПРИ КАКИХ ОБСТОЯТЕЛЬСТВАХ АВТОРЫ ИЛИ АВТОРСКИЕ ПРАВА НЕ ДОЛЖНЫ
ВЛАДЕЛЬЦЫ НЕСУТ ОТВЕТСТВЕННОСТЬ ЗА ЛЮБЫЕ ПРЕТЕНЗИИ, УБЫТКИ ИЛИ ДРУГУЮ ОТВЕТСТВЕННОСТЬ,
В ДЕЙСТВИИ ДОГОВОРА, ДИРЕКТА ИЛИ ДРУГИХ ОБРАЗНЫХ УСЛОВИЯХ, ВОЗНИКАЮЩИХ
ИЗ, ВНЕ ИЛИ В СВЯЗИ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ ИЛИ ИСПОЛЬЗОВАНИЕМ ИЛИ
ДРУГИЕ ДЕЛА В ПРОГРАММНОМ ОБЕСПЕЧЕНИИ.
"""

import math




class Player:
    # Атрибут класса
    # Системная константа, которая ограничивает 
    # изменение волатильности с течением времени.
    _tau = 0.5

    def getRating(self):
        return (self.__rating * 173.7178) + 1500 

    def setRating(self, rating):
        self.__rating = (rating - 1500) / 173.7178

    rating = property(getRating, setRating)

    def getRd(self):
        return self.__rd * 173.7178

    def setRd(self, rd):
        self.__rd = rd / 173.7178

    rd = property(getRd, setRd)

    def __init__(self, rating = 1500, rd = 350, vol = 0.06):
        # В целях тестирования предварительно загрузите значения,
        # присвоенные игроку без рейтинга.
        self.setRating(rating)
        self.setRd(rd)
        self.vol = vol

    def _preRatingRD(self):
        """ Рассчитывает и обновляет отклонение рейтинга игрока для
         начало рейтингового периода.

        preRatingRD() -> None

        """
        self.__rd = math.sqrt(math.pow(self.__rd, 2) + math.pow(self.vol, 2))

    def update_player(self, rating_list, RD_list, outcome_list):
        """ Рассчитывает новый рейтинг и отклонение рейтинга игрока.

        update_player(list[int], list[int], list[bool]) -> None

        """
        # Преобразуйте значения рейтинга и отклонения рейтинга для 
        # внутреннего использования.
        rating_list = [(x - 1500) / 173.7178 for x in rating_list]
        RD_list = [x / 173.7178 for x in RD_list]

        v = self._v(rating_list, RD_list)
        self.vol = self._newVol(rating_list, RD_list, outcome_list, v)
        self._preRatingRD()

        self.__rd = 1 / math.sqrt((1 / math.pow(self.__rd, 2)) + (1 / v))

        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * \
                       (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        self.__rating += math.pow(self.__rd, 2) * tempSum

    #Шаг 5        
    def _newVol(self, rating_list, RD_list, outcome_list, v):
        """ Расчет новой волатильности по системе Glicko2. 

        Updated for Feb 22, 2012 revision. -Leo

        _newVol(list, list, list, float) -> float

        """
        #Шаг 1
        a = math.log(self.vol**2)
        eps = 0.000001
        A = a

        #Шаг 2
        B = None
        delta = self._delta(rating_list, RD_list, outcome_list, v)
        tau = self._tau
        if (delta ** 2)  > ((self.__rd**2) + v):
          B = math.log(delta**2 - self.__rd**2 - v)
        else:        
          k = 1
          while self._f(a - k * math.sqrt(tau**2), delta, v, a) < 0:
            k = k + 1
          B = a - k * math.sqrt(tau **2)

        #Шаг 3
        fA = self._f(A, delta, v, a)
        fB = self._f(B, delta, v, a)

        #Шаг 4
        while math.fabs(B - A) > eps:
          #a
          C = A + ((A - B) * fA)/(fB - fA)
          fC = self._f(C, delta, v, a)
          #b
          if fC * fB <= 0:
            A = B
            fA = fB
          else:
            fA = fA/2.0
          #c
          B = C
          fB = fC

        #Шаг 5
        return math.exp(A / 2)

    def _f(self, x, delta, v, a):
      ex = math.exp(x)
      num1 = ex * (delta**2 - self.__rating**2 - v - ex)
      denom1 = 2 * ((self.__rating**2 + v + ex)**2)
      return  (num1 / denom1) - ((x - a) / (self._tau**2))

    def _delta(self, rating_list, RD_list, outcome_list, v):
        """ Дельта-функция системы Glicko2.

        _delta(list, list, list) -> float

        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        return v * tempSum

    def _v(self, rating_list, RD_list):
        """ Функция v системы Glicko2.

        _v(list[int], list[int]) -> float

        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempE = self._E(rating_list[i], RD_list[i])
            tempSum += math.pow(self._g(RD_list[i]), 2) * tempE * (1 - tempE)
        return 1 / tempSum

    def _E(self, p2rating, p2RD):
        """ Функция Glicko E.

        _E(int) -> float

        """
        return 1 / (1 + math.exp(-1 * self._g(p2RD) * \
                                 (self.__rating - p2rating)))

    def _g(self, RD):
        """ Функция Glicko2 g(RD).

        _g() -> float

        """
        return 1 / math.sqrt(1 + 3 * math.pow(RD, 2) / math.pow(math.pi, 2))

    def did_not_compete(self):
        """ Применяет шаг 6 алгоритма. Используйте это для
        игроков, которые не участвовали в рейтинговом периоде.
        did_not_compete() -> None

        """
        self._preRatingRD()