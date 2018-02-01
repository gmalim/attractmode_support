# MAME support tools for Attract-Mode

This repository contains a collection of programs that provides [MAME](http://www.mamedev.org/) support for the [Attract-Mode](http://www.attractmode.org/) frontend:

- [MAME emulation benchmark generator](#benchgen)
- [MAME emulation benchmark support for Attract-Mode](#benchana)
- [MAME hiscore support for Attract-Mode](#hiscore)
- [MAME bezel artwork support for Attract-Mode](#bezel)
- [MAME game controls support for Attract-Mode](#control)
- [MAME title display and sorting support for Attract-Mode](#title)
- [MAME startup scripts](#start)
- [Attract-Mode layout with abovementioned MAME support (WIP)](#layout)

---
<a name="benchgen" />

### MAME emulation benchmark generator: [*benchmarkgenerator.py*](benchmarkgenerator.py)

Python program to generate MAME emulation benchmark files of a single game or a list of games. Benchmarks are saved in a dedicated MAME benchmarks directory.

Usage: See program docstring

<a name="benchana" />

### MAME benchmark support for Attract-Mode: [*benchmarkanalysis.py*](benchmarkanalysis.py)

Python program to analyze MAME emulation benchmark files of a single game or a list of games:

- Average emulation speed and total emulation time are calculated by taking into account the benchmark from the last game and
  the previous benchmark.
- The previous benchmark is updated and saved in a dedicated MAME benchmarks directory.
- The average emulation speed is converted into a 1-5 star rating. 
- Benchmark data are saved in a formatted ASCII file (**data/AMbenchmarks.ini**). This file can be used to display benchmark data in Attract-Mode.

Usage: See program docstring

<a name="hiscore" />

### MAME hiscore support for Attract-Mode: [*hiscoreanalysis.py*](hiscoreanalysis.py)

Python program to analyze hiscores of a single game or a list of games:

- Binary hiscore data is readout and converted into ASCII code using the [hi2txt](http://greatstone.free.fr/hi2txt/) Java archive.
- The hi2txt output is saved in a dedicated MAME hiscores directory.
- The top hiscore of each game is reformatted and saved in a formatted ASCII file (**data/AMhiscores.ini**). This file can be used to display the top hiscores in Attract-Mode.

Requirements:

- Latest [hiscore.dat](http://highscore.mameworld.info/), and follow instructions to enable hiscore saving in MAME.
- Latest [hi2txt.jar and hi2txt.zip](http://greatstone.free.fr/hi2txt/).
- [Java](https://www.java.com) (to run hi2txt.jar)

Usage: See program docstring

<a name="bezel" />

### MAME bezel artwork support for Attract-Mode: [*bezelanalysis.py*](bezelanalysis.py)

Python program to analyze MAME bezel artwork:

- Analysis is based on the standard .lay file structure as defined [here](http://wiki.mamedev.org/index.php/LAY_File_Basics_-_Part_I).
- User chooses whether to create a low resolution version of each bezel (since bezel files usually are high resolution and therefore can be slow to render in Attract-Mode), or create symbolic links to the original bezel files.
- Low-resolution bezels / symlinks are saved in a dedicated Attract-Mode bezels directory.
- Bezel data are reformatted and saved in a formatted ASCII file (**data/AMbezels.ini**). This file can be used to display bezels in Attract-Mode.

Requirements:

- Bezel artwork, e.g. [http://www.progettosnaps.net/artworks/](http://www.progettosnaps.net/artworks/)
- Each bezel artwork .zip file should be unzipped in its own corresponding directory (use [unziplist.bash](unziplist.bash)).
- Sips (to create low resolution versions of bezels): An command-line image processing tool that is standard installed on Mac OS X. If Sips is not installed, symbolic links to the original bezel files will be created instead. For Linux and Windows users, a great free alternative to Sips is [ImageMagick](https://www.imagemagick.org) - just install and change the code accordingly.

Options:

- [bezelexceptions.txt](data/bezelexceptions.txt): An example file is provided. Unfortunately for some bezels the analysis can give wrong results in Attract-Mode (e.g because the .lay file contains additional xml tags or has a non-standard structure). Games for which the analysis fails should be added to bezelexceptions.txt, the corresponding bezel file in the AM bezels directory should be deleted and bezelanalysis.py should be run again to generate a new AMbezels.ini.

Usage: See program docstring

<a name="control" />

### MAME game controls support for Attract-Mode: [*reformatcontrols.py*](reformatcontrols.py)

Python program to reformat and save game controls data in a formatted ASCII file (**data/AMcontrols.ini**). This file can be used to display game controls data in Attract-Mode.

Requirements:

- Latest [controls.ini](data/controls.ini) file: no longer developed (?), latest version is provided (v0.141.1 taken from [here](http://ledblinky.net/downloads/controls.ini.0.141.1.zip)).

Usage: See program docstring

<a name="title" />

### MAME title display and sorting support for Attract-Mode: [*updateromlist.py*](updateromlist.py)

Python program to update the Attract-Mode MAME romlist with additional game data:

- The *AltTitle* field is replaced by a cleaned title (square and round parentheses as well as any leading "The" or "Vs." are removed) for display purposes in Attract-Mode.
- The *Buttons* field is replaced by a tag that can be used to sort games in Attract-Mode.
- The *Extra* field is replaced by a formatted tag to indicate whether hiscore, benchmark, bezel and/or game controls data are available or not. This can be used to contruct Attract-Mode filters based on these parameters.

Options:

- [AMtitles.txt](data/AMtitles.txt): An example file is provided. Update this file in a text editor if you want to change the order of specific games in Attract-Mode (e.g. if you prefer *umk3* to appear between *mk3* and *mk4*). You can also explicitly add a display title tag to games that are part of a series (e.g. *starwars*, *esb* and *jedi* as part of the same 'Star Wars' series).
- **AMhiscores.ini** generated by [hiscoreanalysis.py](hiscoreanalysis.py)
- **AMbenchmarks.ini** generated by [benchmarkanalysis.py](benchmarkanalysis.py)
- **AMbezels.ini** generated by [bezelanalysis.py](bezelanalysis.py)
- **AMcontrols.ini** generated by [reformatcontrols.py](reformatcontrols.py)

Usage: See program docstring

<a name="start" />

### MAME startup scripts: [*mame.bash*](mame.bash) and [*mame.csh*](mame.csh)

Startup scripts for the sh and csh shell families to automate the execution of [hiscoreanalysis.py](hiscoreanalysis.py) and [benchmarkanalysis.py](benchmarkanalysis.py) immediately after running a MAME game. These scripts can be used to start MAME games in Attract-Mode (i.e. point 'executable' variable in mame.cfg to one of these scripts).

<a name="layout" />

### Attract-Mode layout with abovementioned MAME support (WIP): [*mylayout*](mylayout)

Attract-Mode layout for arcade games emulated with MAME, featuring:

- Current hiscore displayed for each game
- Current emulation benchmark displayed for each game
- Bezel artwork displayed for each game
- Game controls information displayed for each game
- Custom display and sorting titles

Requirements:

- **AMhiscores.ini** generated by [*hiscoreanalysis.py*](hiscoreanalysis.py)
- **AMbenchmarks.ini** generated by [*benchmarkanalysis.py*](benchmarkanalysis.py)
- **AMbezels.ini** generated by [*bezelanalysis.py*](bezelanalysis.py)
- **AMcontrols.ini** generated by [*reformatcontrols.py*](reformatcontrols.py)
- An updated romlist generated by [*updateromlist.py*](updateromlist.py)
