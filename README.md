# ZFW Rolling Call Macros

This script maps hotkeys to the rolling call alias for VRC. Gives the option to configure your own hotkeys and change departure sectors easily as controllers logon.

## Getting Started

Clone the repo and install the libraries in `requirements.txt` ideally in a fresh virtual environment.

```
git clone https:\\ ; cd
```
```
pip install -r requirements.txt
```

## Functionality

The script works by instantly typing the rolling call alias: 
```
.d {departure_sector_id} {runway}
```

The `config.json` file is where keybindings can be configured. By default there are six `facility-flow` groups: `dfw-south`, `dfw-north`, `dal-south`, `dal-north`, `okc-south`, `okc-north`. 

Each group contains a default departure sector ID set to `51` corresponding to `Choctaw-Ultra-High`. Each group also contains a keybind-to-runway dictionary. Here you can change the keybindings for each runway. Special character names can be found [here](https://github.com/boppreh/keyboard/blob/e277e3f2baf53ee1d7901cbb562f443f8f861b90/keyboard/_canonical_names.py#L12).

## Running

To run the script, run the following line in cmd:

```
python macro.py -f FACILITY-FLOW
```

`FACILITY-FLOW` should be replaced with the name corresponding group you intend to control named above or any new groups added to the config file.

## Changing Departure Sector ID

Once the script runs, you will be prompted to enter a new departure sector ID. If you want a different departure sector ID while the program is running, you can type it in the terminal following the prompt. You can also change the default departure sector ID in the `config.json` file.