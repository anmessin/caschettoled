import cmd2

from colorama import Fore, Style
from littlehardhat import LittleHardHat, LittleHardHatError

class LittleHardHatCLI(cmd2.Cmd):

    # =====================================================
    # Construction.
    # =====================================================
    def __init__(self, board: LittleHardHat):
        super().__init__()
        self.board = board
        self.prompt = "LHH> "

        cmd2.categorize(
            (cmd2.Cmd.do_alias, cmd2.Cmd.do_help, cmd2.Cmd.do_history, cmd2.Cmd.do_quit, cmd2.Cmd.do_set, cmd2.Cmd.do_run_script, cmd2.Cmd.do_shell),
            "General commands"
        )

        # -- Channels -------------------------------------------------------------
        self.ch_min, self.ch_max = self.board.VALID_CHANNEL_RANGE
        self.all_channels = range(self.ch_min, self.ch_max + 1)

    def prsuccess(self, msg) -> None:
        self.poutput(msg)

    # =====================================================
    # ON: Turn on DAC.
    # =====================================================
    on_parser = cmd2.Cmd2ArgumentParser()
    on_parser.add_argument('channel', type=int, nargs='*', help="Single channel to turn on (1-19).")
    on_parser.add_argument('-v', '--value', type=int, default=2048, help="DAC value (1-4095).")
    on_parser.add_argument('-a', '--all', action="store_true", help='turn on all channels')

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(on_parser)
    def do_on(self, args):
        """Turn on one or more channels DAC by setting the value."""

        if (not args.all) and (not args.channel):
            self.perror("Error: specify at least one channel or use -a.")
            return

        channels = (self.all_channels if args.all else args.channel)

        for ch in channels:
            try:
                self.board.set_dac(ch,args.value)
                self.prsuccess(f"Channel {ch} turned on to {args.value}.")
            except LittleHardHatError as e:
                self.perror(f"[ch {ch}] {e}")
        
    # =====================================================
    # OFF: Turn off DAC.
    # =====================================================
    off_parser = cmd2.Cmd2ArgumentParser()
    off_parser.add_argument('channel', type=int, nargs='*', help="Single channel to turn off (1-19).")
    off_parser.add_argument('-a', "--all", action="store_true", help='turn off all channels')

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(off_parser)
    def do_off(self, args):
        """Turn off one or more channels DAC."""

        if (not args.all) and (not args.channel):
            self.perror("Error: specify at least one channel or use -a.")
            return
        
        channels = (self.all_channels if args.all else args.channel)

        for ch in channels:
            try:
                self.board.set_dac(ch,0)
                self.prsuccess(f"Channel {ch} turned off.")
            except LittleHardHatError as e:
                self.perror(f"[ch {ch}] {e}")

    # =====================================================
    # TRIGGER: Set the parameters of the trigger.
    # =====================================================
    trigger_parser = cmd2.Cmd2ArgumentParser()
    trigger_parser.add_argument('frequency', type=int, nargs='?', help="Frequency of the internal trigger in Hz (1,000-10,000)")
    trigger_parser.add_argument('-e', '--external', action='store_true', default=False, help="Source of the trigger ('internal' or 'external')")

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(trigger_parser)
    def do_trigger(self, args):
        """Set frequency of the internal trigger."""

        if args.frequency is None and not args.external:
            self.perror("Error: Specify a frequency or use -e for external source.")
            return

        if args.frequency is not None and args.external:
            self.perror(f"Error: Cannot specify both frequency and external source")
            return
        
        try:
            if args.external:
                self.board.set_trigger_source('external')
            else:
                self.board.set_trigger_source('internal')
                self.board.set_frequency(args.frequency)
            self.prsuccess(f"Trigger source set to external." if args.external else f"Trigger set to {args.frequency} Hz")
        
        except LittleHardHatError as e:
            self.perror(f"Error: {e}")

    # =====================================================
    # SWEEP: Set the range of the sweep.
    # =====================================================
    adjsweep_parser = cmd2.Cmd2ArgumentParser()
    adjsweep_parser.add_argument('min', type=int, help="Lower bound of the sweep range.")
    adjsweep_parser.add_argument('max', type=int, help="Upper bound of the sweep range.")

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(adjsweep_parser)
    def do_adjsweep(self, args):
        """Set min and max range of the sweep."""
        
        if args.max <= args.min:
            self.perror("Error: max cannot be less than min or equal.")
            return
        
        try:
            self.board.set_sweep_min(args.min)
            self.board.set_sweep_max(args.max)
            self.prsuccess(f"Range Sweep set to [{args.min},{args.max}]")

        except LittleHardHatError as e:
            self.perror(f"Error: {e}")

    # =====================================================
    # SWEEP: Turn off/on/loop the sweep for single channel.
    # =====================================================
    sweep_parser = cmd2.Cmd2ArgumentParser()
    sweep_parser.add_argument('mode', type=str, choices=['off','on', 'loop'], help="Mode for the sweep (on,off,loop).")
    sweep_parser.add_argument('channel', type=int, help="Single channel to turn off (1-19).")
    sweep_parser.add_argument('-n', '--nstep', type=int, default=None, help="Number of DAC steps across the sweep range.")
    sweep_parser.add_argument('-t', '--time', type=int, default=None, help="Duration of each step in milliseconds.")

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(sweep_parser)
    def do_sweep(self, args):
        """Turn off/on/loop the sweep for single channel."""

        try: 
            kwargs = {}
            if args.nstep is not None:   
                kwargs['NumberOfStep'] = args.nstep
            if args.time is not None:   
                kwargs['TimeForStep']  = args.time

            self.board.set_sweep(args.channel,args.mode,**kwargs)
            self.prsuccess(f"Channel {args.channel} sweep set to '{args.mode}'" + (f" [nstep={args.nstep}, time={args.time}ms]" if args.nstep else "") + ".")

        except LittleHardHatError as e:
            self.perror(f"Error: {e}")

    # =====================================================
    # TEMPERATURE: Set temperature of the heater.
    # =====================================================
    temperature_parser = cmd2.Cmd2ArgumentParser()
    temperature_parser.add_argument('temperature', type=float, help="Temperature of the heater.")

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(temperature_parser)
    def do_temperature(self, args):
        """Set the temperature in °C of the heater on the board."""

        try:
            self.board.set_temperature(args.temperature)
            self.prsuccess(f"Temperature set to {args.temperature} °C.")

        except LittleHardHatError as e:
            self.perror(f"Error: {e}")

    # =====================================================
    # HEATER: Set power of the heater.
    # =====================================================
    powerheater_parser = cmd2.Cmd2ArgumentParser()
    powerheater_parser.add_argument('power', type=int, help="Power of the heater.")

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(powerheater_parser)
    def do_heater(self, args):
        """Set the power of the heater on the board."""

        try:
            self.board.set_heater_power(args.power)
            self.prsuccess(f"Heater power set to {args.power}.")

        except LittleHardHatError as e:
            self.perror(f"Error: {e}")

    # =====================================================
    # RESET: Reset board to default parameters.
    # =====================================================
    reset_parser = cmd2.Cmd2ArgumentParser()
    
    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(reset_parser)
    def do_reset(self, args):
        """Reset board to default parameters."""
        
        for ch in self.all_channels:
            self.board.set_dac(ch,0)
            
        self.board.set_frequency(1000)

        self.prsuccess("Board reset to default parameters.")

    # =====================================================
    # STATUS: Print channel status.
    # =====================================================
    @cmd2.with_category("Monitoring commands")
    def do_status(self, _):
        """
        Show 19 channel status with DAC info.

        Example output:
            "Legend: '.': off, '-': on, '>': sweep on, '@': sweep loop"                                                                            
                                                                                                                        
                 12.  01.  02.              0000  0000  0000                                                                
               11.  18.  13.  03.        0000  0000  0000  0000                                                              
            10.  17.  19.  14.  04.   0000  0000  0000  0000  0000                                                        
               09.  16.  15.  05.        0000  0000  0000  0000                                                              
                 08.  07.  06.             0000  0000  0000      

            JS_Trigger_Frequency: 1000                                                                                    
            JS_Sweep: off                                                                                                 
            JS_SweepAdjmin: 1000                                                                                          
            JS_SweepAdjMAX: 3000                                                                                          
            JS_NumberOfStep: 0                                                                                            
            JS_TimeForStep: 100                                                                                            
        """

        off, on, sweep_on, sweep_loop = ".", "-", ">", "@"
        status_json = self.board.get_status_dac()

        def general_info():
            info = {key: value for key, value in status_json.items() if not key.startswith('JS_Channel')}
            for key, value in info.items():
                print(f"-{key[3:]}: {value}")

        def status(channel: int):
            dac_value = status_json[f"JS_Channel_{channel}"]
            ch_sweep = status_json["JS_SelectedCh"]
            sweep_mode = status_json["JS_Sweep"]

            if dac_value == 0:
                color, symbol = Fore.RED, off
            elif channel == ch_sweep and sweep_mode == "single":
                color, symbol = Fore.BLUE, sweep_on
            elif channel == ch_sweep and sweep_mode == "loop":
                color, symbol = Fore.CYAN, sweep_loop
            else:
                color, symbol = Fore.GREEN, on

            channel_status = color + f"{channel:02}{symbol}" + Style.RESET_ALL
            dac_value      = color + f"{dac_value:04}" + Style.RESET_ALL
            
            return channel_status, dac_value
        
        stat = {ch: status(ch) for ch in self.all_channels}

        off_legend        = Fore.RED   + f"off='{off}'"               + Style.RESET_ALL
        on_legend         = Fore.GREEN + f"on='{on}'"                 + Style.RESET_ALL
        sweep_on_legend   = Fore.BLUE  + f"sweep on='{sweep_on}'"     + Style.RESET_ALL
        sweep_loop_legend = Fore.CYAN  + f"sweep loop='{sweep_loop}'" + Style.RESET_ALL

        status_scheme = [
            f"      {stat[12][0]}  {stat[1][0]}  {stat[2][0]}",
            f"   {stat[11][0]}  {stat[18][0]}  {stat[13][0]}  {stat[3][0]}",
            f"{stat[10][0]}  {stat[17][0]}  {stat[19][0]}  {stat[14][0]}  {stat[4][0]}",
            f"   {stat[9][0]}  {stat[16][0]}  {stat[15][0]}  {stat[5][0]}",
            f"      {stat[8][0]}  {stat[7][0]}  {stat[6][0]}",
        ]

        dac_scheme = [
            f"          {stat[12][1]}  {stat[1][1]}  {stat[2][1]}",
            f"     {stat[11][1]}  {stat[18][1]}  {stat[13][1]}  {stat[3][1]}",
            f"{stat[10][1]}  {stat[17][1]}  {stat[19][1]}  {stat[14][1]}  {stat[4][1]}",
            f"     {stat[9][1]}  {stat[16][1]}  {stat[15][1]}  {stat[5][1]}",
            f"          {stat[8][1]}  {stat[7][1]}  {stat[6][1]}",
        ]

        self.poutput()
        self.poutput(f"Legend: {off_legend}, {on_legend}, {sweep_on_legend}, {sweep_loop_legend}")
        self.poutput()
        for ch, dac in zip(status_scheme, dac_scheme):
            self.poutput(ch, " ", dac)
        self.poutput()
        general_info()
        self.poutput()