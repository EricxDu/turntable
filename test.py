import turntable

player = turntable.TurnTable("pi")
player.play()

# loop until finished
while True:
    command = input("Enter command: ")
    if command == "minus":
        player.minus()
    elif command == "next":
        player.next()
    elif command == "plus":
        player.plus()
    elif command == "skip":
        player.skip()
    elif command == "alb":
        print(player.get_alb())
    elif command == "art":
        print(player.get_art())
    elif command == "long":
        print(player.get_long())
    elif command == "name":
        print(player.get_name())
    elif command == "pos":
        print(player.get_pos())
    elif command == "time":
        print(player.get_time())
    elif command == "vol":
        print(player.get_vol())
