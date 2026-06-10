import os
import cmd2

from dotenv import load_dotenv
from littlehardhat import LittleHardHat
from commands import LittleHardHatCLI

def banner(host, timeout):
    BANNER = [
        f"Little Hard Hat - Control Interface",
        f" _      _    _ _    _ ",
        f"| |    | |  | | |  | |",
        f"| |    | |__| | |__| |",
        f"| |    |  __  |  __  |",
        f"| |____| |  | | |  | |",
        f"|______|_|  |_|_|  |_|",
        f"",
        f"Host: {host}",
        f"Timeout: {timeout}s"
    ]

    for line in BANNER:
        print(line)
                           
def main():

    parser = cmd2.Cmd2ArgumentParser()
    parser.add_argument('--timeout', type=int, default=5)
    args = parser.parse_args()

    load_dotenv()
    host = os.getenv("LHHBOARD1_IP")

    board = LittleHardHat(host, args.timeout)

    banner(host, args.timeout)
    cli = LittleHardHatCLI(board)
    cli.cmdloop()

if __name__ == "__main__":
    main()