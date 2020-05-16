import random
import sys
from time import sleep

LIMIT = 16


class Collision (Exception):
    pass


class Station:
    def __init__(self, name, cable):
        self.name = name
        self.collision_num = 0
        self.wait = 0
        self.cable = cable
        self.idle = 1
        self.sent = 0

    def received(self, position):
        if self.name == "Station_A" and position == len(self.cable)-1:
            return True
        elif self.name == "Station_B" and position == 0:
            return True

    def back_off(self):
        if self.collision_num >= 10:
            self.wait = random.randint(0, (2**10)-1)
        elif self.collision_num > LIMIT:
            pass
        else:
            self.wait = random.randint(0, (2 ** self.collision_num) - 1)

    def carrier_idle(self, cable):
        for i in cable:
            if i == '<' or i == '>':
                self.idle = 0
                return self.idle
            else:
                return self.idle


class Cable:
    def __init__(self, cable):
        self.idle = 1
        self.wait = 0
        self.length = len(cable)-1
        self.cable = cable

    def __str__(self):
        pass

    def clear(self):
        for i in range(len(self.cable)):
            self.cable[i] = '_'
        return 0, self.length

    def push_left(self, position):
        if position == self.length:
            self.clear()
            return position
        elif self.cable[position] == '<':
            raise Collision
        else:
            self.cable[position] = '>'
            return position+1

    def push_right(self, position):
        if position == 0:
            self.clear()
            return position
        elif self.cable[position] == '>':
            raise Collision
        else:
            self.cable[position] = '<'
            return position-1


def main():
    cable = Cable(['_' for _ in range(10)])
    station_A = Station("Station_A", cable.cable)
    station_B = Station("Station_B", cable.cable)

    position_A = 0
    position_B = cable.length
    station_A.sent = 1
    station_B.sent = 1

    while True:

        if station_A.carrier_idle(cable.cable) and station_B.carrier_idle(cable.cable):
            if station_A.wait == 0 and station_B.wait == 0:
                while not (station_A.received(position_A) and station_B.received(position_B)):
                    try:
                        if station_A.sent == 1:
                            position_A = cable.push_left(position_A)
                            if station_A.received(position_A):
                                station_A.sent = 0
                                cable.cable[position_A] = 'sent'
                                print(cable.cable)
                                sys.exit()
                        if station_B.sent == 1:
                            position_B = cable.push_right(position_B)
                            if station_B.received(position_B):
                                station_B.sent = 0
                                cable.cable[position_B] = 'sent'
                                print(cable.cable)
                                sys.exit()
                        print(cable.cable)
                    except Collision:
                        position_A, position_B = cable.clear()
                        station_A.collision_num += 1
                        station_B.collision_num += 1
                        station_A.back_off()
                        station_B.back_off()
                        break
                continue

            if station_A.wait == 0 and (station_A.wait < station_B.wait) and station_A.sent == 1:
                while not station_A.received(position_A):
                    position_A = cable.push_left(position_A)
                    print(cable.cable)
                cable.cable[position_A] = 'sent'
                print(cable.cable)
                station_A.sent = 0
                position_A, position_B = cable.clear()

            if station_B.wait == 0 and (station_B.wait < station_A.wait) and station_B.sent == 1:
                while not station_B.received(position_B):
                    position_B = cable.push_right(position_B)
                    print(cable.cable)
                cable.cable[position_B] = 'sent'
                print(cable.cable)
                station_B.sent = 0
                position_A, position_B = cable.clear()

        if station_A.wait != 0:
            station_A.wait -= 1
        if station_B.wait != 0:
            station_B.wait -= 1


if __name__ == "__main__":
    main()
