import time
import redis


from screen import Screen
from analyzer import Analyzer

screen = Screen()
analyzer = Analyzer()

con = redis.Redis("localhost")


def main():
    bark = analyzer.get_bark()
    screen.update(bark)
    print(con.get("mode").decode("utf-8"))

if __name__ == "__main__":
    count = 0
    while True:
        main()
        count += 1
    screen.close()
    analyzer.close()
