import os
import cmd2
import sys

from dotenv import load_dotenv
from commands import LittleHardHatCLI
from littlehardhat import (
    LittleHardHat,
    LittleHardHatError,
    LittleHardHatConnectionError,
    LittleHardHatTimeoutError,
    LittleHardHatResponseError,
)

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
    parser.add_argument('--board', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=2)
    args = parser.parse_args()

    load_dotenv()

    env_key = f"LHHBOARD{args.board}_IP"
    host = os.getenv(env_key)
    board = LittleHardHat(host, args.timeout)

    if not host:
        raise ValueError(f"Board {args.board} not found.")

    sys.argv = [sys.argv[0]]

    banner(host, args.timeout)
    cli = LittleHardHatCLI(board, args.board)
    cli.cmdloop()

if __name__ == "__main__":
    main()