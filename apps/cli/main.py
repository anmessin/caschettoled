import os
import cmd2

from dotenv import load_dotenv
from littlehardhat import LittleHardHat
from commands import LittleHardHatCLI

def main():

    parser = cmd2.Cmd2ArgumentParser()
    parser.add_argument('--timeout', type=int, default=5)
    args = parser.parse_args()

    load_dotenv()
    host1 = os.getenv("LHHBOARD1_IP")
    host2 = os.getenv("LHHBOARD2_IP")

    board = LittleHardHat(host2, args.timeout)

    cli = LittleHardHatCLI(board)
    cli.cmdloop()

if __name__ == "__main__":
    main()