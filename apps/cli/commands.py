import cmd2
import time

from colorama import Fore, Style
from littlehardhat import (
    LittleHardHat,
    LittleHardHatError,
    LittleHardHatConnectionError,
    LittleHardHatTimeoutError,
    LittleHardHatResponseError,
)

class LittleHardHatCLI(cmd2.Cmd):
    # =====================================================
    # Constructor.
    # =====================================================
    def __init__(self, board: LittleHardHat, board_id: int):
        super().__init__()

        self.board = board
        self.board_id = board_id
        self.prompt = f"LHH[{board_id}]> "

        cmd2.categorize(
            (
                cmd2.Cmd.do_alias,     
                cmd2.Cmd.do_help,      
                cmd2.Cmd.do_history,   
                cmd2.Cmd.do_quit,      
                cmd2.Cmd.do_set,       
                cmd2.Cmd.do_run_script,
                cmd2.Cmd.do_shell      
            ),
            "General commands"
        )

        # -- Channels -------------------------------------------------------------
        self.ch_min, self.ch_max = self.board.VALID_CHANNEL_RANGE
        self.all_channels = range(self.ch_min, self.ch_max + 1)

    def prsuccess(self, msg):
        self.poutput(Fore.GREEN + msg + Style.RESET_ALL)

    # =====================================================
    # ON: Turn on DAC.
    # =====================================================
    on_parser = cmd2.Cmd2ArgumentParser()
    on_parser.add_argument('channel', type=int, nargs='*', help="Single channel to turn on (1-19).")
    on_parser.add_argument('--value', type=int, default=2048, help="DAC value (1-4095).")
    on_parser.add_argument('--all', action="store_true", help='turn on all channels')

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(on_parser)
    def do_on(self, args):
        """Turn on one or more channels DAC by setting the value."""

        if (not args.all) and (not args.channel):
            self.perror("Error: specify at least one channel or use --all.")
            return

        if args.value == 0:
            self.perror(f"Error: --value cannot be 0; use 'off' to turn off a channel.")
            return

        channels = (self.all_channels if args.all else args.channel)

        for ch in channels:
            try:
                self.board.set_dac(ch, args.value)
                status_dac = self.board.fetch_status_dac()
                dac_value = status_dac[f"JS_Channel_{ch}"]

                if args.value == dac_value:
                    self.prsuccess(f"Channel {ch} turned on to {args.value}.")
                else: 
                    self.perror(f"[ch {ch}] Board error: Channel {ch} turned on to {dac_value} instead of {args.value}.")

            except (TypeError, ValueError) as e:
                self.perror(f"[ch {ch}] Invalid input: {e}")
            except LittleHardHatError as e:
                self.perror(f"[ch {ch}] Board error: {e}")

    # =====================================================
    # OFF: Turn off DAC.
    # =====================================================
    off_parser = cmd2.Cmd2ArgumentParser()
    off_parser.add_argument('channel', type=int, nargs='*', help="Single channel to turn off (1-19).")
    off_parser.add_argument("--all", action="store_true", help='turn off all channels')

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(off_parser)
    def do_off(self, args):
        """Turn off one or more channels DAC."""

        if (not args.all) and (not args.channel):
            self.perror("Error: specify at least one channel or use --all.")
            return
        
        channels = (self.all_channels if args.all else args.channel)

        for ch in channels:
            try:
                self.board.set_dac(ch,0)
                status_dac = self.board.fetch_status_dac()
                dac_value = status_dac[f"JS_Channel_{ch}"]

                if 0 == dac_value:
                    self.prsuccess(f"Channel {ch} turned off.")
                else: 
                    self.perror(f"[ch {ch}] Board error: Channel {ch} not turned off. Set to {dac_value}.")

            except (TypeError, ValueError) as e:
                self.perror(f"[ch {ch}] Invalid input: {e}")
            except LittleHardHatError as e:
                self.perror(f"[ch {ch}] Board error: {e}")

    # =====================================================
    # TRIGGER: Set the parameters of the trigger.
    # =====================================================
    trigger_parser = cmd2.Cmd2ArgumentParser()
    trigger_parser.add_argument('frequency', type=int, nargs='?', help="Frequency of the internal trigger in Hz (1,000-10,000)")
    trigger_parser.add_argument('--external', action='store_true', default=False, help="Source of the trigger ('internal' or 'external')")

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(trigger_parser)
    def do_trigger(self, args):
        """Set frequency of the internal trigger."""

        if args.frequency is None and not args.external:
            self.perror("Error: Specify a frequency or use --external for external source.")
            return

        if args.frequency is not None and args.external:
            self.perror(f"Error: Cannot specify both frequency and external source.")
            return
        
        try:
            if args.external:
                self.board.set_trigger_source('external')
                self.prsuccess(f"Trigger source set to external.")
            else:
                self.board.set_trigger_source('internal')
                self.board.set_frequency(args.frequency)
                status_dac = self.board.fetch_status_dac()
                trigger_value = status_dac[f"JS_Trigger_Frequency"]

                if args.frequency == trigger_value:
                    self.prsuccess(f"Trigger set to {args.frequency} Hz")
                else:
                    self.perror(f"Board Error: Trigger set to {trigger_value} Hz instead of {args.frequency} Hz.")

        except (TypeError, ValueError) as e:
            self.perror(f"{e}")
        except LittleHardHatError as e:
            self.perror(f"Board error: {e}")

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

            status_dac = self.board.fetch_status_dac()
            min_sweep = status_dac[f"JS_SweepAdjmin"]
            max_sweep = status_dac[f"JS_SweepAdjMAX"]
            
            if min_sweep != args.min or max_sweep != args.max:
                self.perror(f"Board error: Range Sweep set to [{min_sweep},{max_sweep}] instead of [{args.min},{args.max}].")
            else:
                self.prsuccess(f"Range Sweep set to [{args.min},{args.max}].")

        except (TypeError, ValueError) as e:
            self.perror(f"{e}")
        except LittleHardHatError as e:
            self.perror(f"Board error: {e}")

    # =====================================================
    # SWEEP: Turn off/on/loop the sweep for single channel.
    # =====================================================
    sweep_parser = cmd2.Cmd2ArgumentParser()
    sweep_parser.add_argument('mode', type=str, choices=['off','on', 'loop'], help="Mode for the sweep (on,off,loop).")
    sweep_parser.add_argument('channel', type=int, help="Single channel to control sweep (1-19).")
    sweep_parser.add_argument('--nstep', type=int, default=None, help="Number of DAC steps across the sweep range.")
    sweep_parser.add_argument('--tstep', type=int, default=None, help="Duration of each step in milliseconds.")

    @cmd2.with_category("Slow control commands")
    @cmd2.with_argparser(sweep_parser)
    def do_sweep(self, args):
        """Turn off/on/loop the sweep for single channel."""

        try: 
            kwargs = {}
            if args.nstep is not None:   
                kwargs['NumberOfStep'] = args.nstep
            if args.tstep is not None:   
                kwargs['TimeForStep']  = args.tstep

            self.board.set_sweep(args.channel,args.mode,**kwargs)
            self.prsuccess(f"Channel {args.channel} sweep set to '{args.mode}'" + (f" [nstep={args.nstep}, time={args.tstep}ms]" if args.nstep else "") + ".")

        except (TypeError, ValueError) as e:
            self.perror(f"{e}")
        except LittleHardHatError as e:
            self.perror(f"[ch {args.channel}] Board error: {e}")

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
            status_temp = self.board.fetch_status_temp()
            temperature_value = status_temp["JS_TSetted"]

            if temperature_value == args.temperature:
                self.prsuccess(f"Temperature set to {args.temperature} °C.")
            else:
                self.perror(f"Board Error: Temperature set to {temperature_value} °C. instead of {args.temperature}.")

        except (TypeError, ValueError) as e:
            self.perror(f"{e}")
        except LittleHardHatError as e:
            self.perror(f"Board error: {e}")

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

        except (TypeError, ValueError) as e:
            self.perror(f"{e}")
        except LittleHardHatError as e:
            self.perror(f"Board error: {e}")

    # =====================================================
    # RENDER METHODS.
    # =====================================================
    def _render_status_dac(self):
        off, on, sweep_on, sweep_loop = ".", "-", ">", "@"
        status_json = self.board.fetch_status_dac()

        def general_info():
            info = {k: v for k, v in status_json.items() if not k.startswith('JS_Channel')}
            return [f"-{k[3:]}: {v}" for k, v in info.items()]
            
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

        lines = []
        lines.append("=== DAC STATUS ===")
        lines.append(f"Legend: {off_legend}, {on_legend}, {sweep_on_legend}, {sweep_loop_legend}")
        lines.append("")
        for ch, dac in zip(status_scheme, dac_scheme):
            lines.append(f"{ch}   {dac}")

        lines.append("")
        lines.extend(general_info())
        lines.append("")

        return lines
    
    def _render_status_temperature(self):

        status_temp_json = self.board.fetch_status_temp()

        temp_channels_scheme = [
            f"-- Channels ------------------",
            f"Ch0  {status_temp_json['JS_T_Ch0']:5.2f} °C    Ch4  {status_temp_json['JS_T_Ch4']:5.2f} °C",
            f"Ch1  {status_temp_json['JS_T_Ch1']:5.2f} °C    Ch5  {status_temp_json['JS_T_Ch5']:5.2f} °C",
            f"Ch2  {status_temp_json['JS_T_Ch2']:5.2f} °C    Ch6  {status_temp_json['JS_T_Ch6']:5.2f} °C",
            f"Ch3  {status_temp_json['JS_T_Ch3']:5.2f} °C    Ch7  {status_temp_json['JS_T_Ch7']:5.2f} °C"
        ]

        temp_board_scheme = [
            f"-- Board -----",
            f"T1    {status_temp_json['JS_T1_Board']:5.2f} °C",
            f"T2    {status_temp_json['JS_T2_Board']:5.2f} °C",
            f"Mean  {status_temp_json['JS_T_Average']:5.2f} °C",
            f"Set   {status_temp_json['JS_TSetted']:5.2f} °C"
        ]

        temp_pid_scheme = [
            f"-- PID -------",
            f"P     {status_temp_json['JS_P_Part']:8.2f}",
            f"I     {status_temp_json['JS_I_Part']:8.2f}",
            f"D     {status_temp_json['JS_D_Part']:8.2f}",
            f"Error {status_temp_json['JS_PID_Error']:8.2f}",
        ]

        lines = []
        lines.append("=== TEMPERATURE STATUS ===")
        lines.append("")
        for temp_ch, temp_board, params_pid in zip(temp_channels_scheme, temp_board_scheme, temp_pid_scheme):
            lines.append(f"{temp_ch}   {temp_board}   {params_pid}")

        lines.append("")

        return lines

    # =====================================================
    # CHANNEL STATUS: Print channel status.
    # =====================================================
    @cmd2.with_category("Monitoring commands")
    def do_status_dac(self, _):
        """Show 19 channel status with DAC info."""

        try: 
            for line in self._render_status_dac():
                self.poutput(line)
        except LittleHardHatError as e:
            self.perror(f"{e}")

    # =====================================================
    # TEMPERATURE STATUS: Print board temperature status.
    # =====================================================
    @cmd2.with_category("Monitoring commands")
    def do_status_temp(self, _):
        """Show tempearature, heater and PID status of the board."""

        try:
            for line in self._render_status_temperature():
                self.poutput(line)
        except LittleHardHatError as e:
            self.perror(f"{e}")

    # =====================================================
    # MONITORING
    # =====================================================
    monitor_parser = cmd2.Cmd2ArgumentParser()
    monitor_parser.add_argument('--dac', action='store_true', help='Show DAC status')
    monitor_parser.add_argument('--temp', action='store_true', help='Show temperature status')
    monitor_parser.add_argument('--rate', type=float, default=1.0, help='Refresh rate in seconds')

    @cmd2.with_category("Monitoring commands")
    @cmd2.with_argparser(monitor_parser)
    def do_monitor(self, args):
        """Live monitor for DAC and/or temperature status (Ctrl+C to stop)."""

        show_dac = args.dac
        show_temp = args.temp
        rate = args.rate

        if not show_dac and not show_temp:
            show_dac = True

        try:
            print("\033[2J", end="")
            print("\033[?25l", end="")

            while True:
                print("\033[H", end="")

                self.poutput(f"[MONITOR] refresh = {rate}s   (Ctrl+C to stop)\n")

                try: 
                    if show_dac:
                        for line in self._render_status_dac():
                            self.poutput(line)

                    if show_temp:
                        for line in self._render_status_temperature():
                            self.poutput(line)
                except LittleHardHatError as e:
                    self.perror(f"{e}")

                time.sleep(rate)

        except KeyboardInterrupt:
            pass

        finally:
            print("\033[?25h", end="")
            self.poutput("\nMonitor stopped.")