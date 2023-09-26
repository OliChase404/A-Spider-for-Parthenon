from rich import print
from rich.console import Console
import os

terminal_width = os.get_terminal_size().columns
console = Console()

def banner():
    print('-' * int(terminal_width / 2))
    console.print("""
   [bright_red]

   ____  _ _ _        _____       _     _           
  / __ \| (_| )      / ____|     (_)   | |          
 | |  | | |_|/ ___  | (___  _ __  _  __| | ___ _ __ 
 | |  | | | | / __|  \___ \| '_ \| |/ _` |/ _ \ '__|
 | |__| | | | \__ \  ____) | |_) | | (_| |  __/ |   
  \____/|_|_| |___/ |_____/| .__/|_|\__,_|\___|_|   
      |                |   | |           |           
      |                |   |_|           |           
      |                |                 |
      |                |                 |
     _|_              _|_               _|_    
///\(o_o)/\\\\\\    ///\(o_o)/\\\\\\     ///\(o_o)/\\\\\\
|||  ` '  |||    |||  ` '  |||     |||  ` '  |||

                                                    V0.1            
      """)
    print('-' * int(terminal_width / 2))