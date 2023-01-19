import receiver, sys, os

if __name__ == '__main__':
    try:
        output = receiver.receive()
        print(output)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)