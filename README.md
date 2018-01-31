# MAME support tools for Attract-Mode

This repository contains a collection of programs that provides [MAME](http://www.mamedev.org/) support for the [Attract-Mode](http://www.attractmode.org/) frontend:

- [MAME hiscore support for Attract-Mode](#hiscore)
- [MAME benchmark generator](#benchgen)
- [MAME benchmark support for Attract-Mode](#benchana)
- [MAME bezel artwork support for Attract-Mode](#bezel)
- [MAME controls support for Attract-Mode](#control)
- [MAME title display and sorting support for Attract-Mode](#title)
- [MAME startup scripts](#start)
- [New Attract-Mode layout with above functionality](#layout)

---
<a name="hiscore" />

### MAME hiscore support for Attract-Mode: [*hiscoreanalysis.py*](hiscoreanalysis.py)

Python program to process hiscores of a single game or a list of games. For each game:

- Binary hiscore data is readout and converted into ASCII code using the [***hi2txt***](http://greatstone.free.fr/hi2txt/) Java archive.
- The hi2txt output is saved in a dedicated MAME hiscores directory.
- The top hiscore is reformatted and saved in a formatted ASCII file (**AMhiscores.ini**).
- This allows hiscores to be displayed in Attract-Mode.

Requirements:

- **hi2txt.jar** and **hi2txt.zip**: [http://greatstone.free.fr/hi2txt](http://greatstone.free.fr/hi2txt/)
- Java: [https://www.java.com](https://www.java.com)
- **hiscore.dat**: [http://highscore.mameworld.info/](http://highscore.mameworld.info/)

<a name="benchgen" />

### MAME benchmark generator: [*benchmarkgenerator.py*](benchmarkgenerator.py)

Python program to generate MAME benchmark files of a single game or a list of games. Benchmarks are saved in a dedicated MAME benchmarks directory.

<a name="benchana" />

### MAME benchmark support for Attract-Mode: [*benchmarkanalysis.py*](benchmarkanalysis.py)

Python program to analyze MAME benchmark files of a single game or a list of games. For each game:

- Average emulation speed and total emulation time are calculated by taking into account the benchmark from the last game and
  the previous benchmark.
- The previous benchmark is updated and saved in a dedicated MAME benchmarks directory.
- The average emulation speed is converted into a 1-5 star rating. 
- Benchmark data are saved in a formatted ASCII file (**AMbenchmarks.ini**).
- This allows benchmark data to be displayed in Attract-Mode.  

<a name="bezel" />

### MAME bezel artwork support for Attract-Mode: [*bezelanalysis.py*](bezelanalysis.py)

Python program to analyze MAME bezel artwork:

- Analysis is based on the standard .lay file structure as defined [here](http://wiki.mamedev.org/index.php/LAY_File_Basics_-_Part_I).
- A lower resolution version of each bezel is saved in a dedicated Attract-Mode bezels directory.
- Bezel data is reformatted and saved in a formatted ASCII file (**AMbezels.ini**).
- This allows bezel artwork to be displayed in Attract-Mode.

Requirements:

- Bezel artwork, e.g. [http://www.progettosnaps.net/artworks/](http://www.progettosnaps.net/artworks/)
- Each bezel artwork .zip file should be unzipped in a corresponding directory (use [*unziplist.bash*](unziplist.bash)).
- Sips: An command-line image processing tool that is standard installed on Mac OS X. For Linux and Windows users, a great free alternative is [ImageMagick](https://www.imagemagick.org) - just install and change the code accordingly.

<a name="control" />

### MAME controls support for Attract-Mode: [*controlanalysis.py*](controlanalysis.py)

Python program to analyze game controls:

- Control data is reformatted and saved in a formatted ASCII file (**AMcontrols.ini**).
- This allows game controls to be displayed in Attract-Mode.

Requirements:

- **controls.ini**, e.g. [http://ledblinky.net/downloads/controls.ini.0.141.1.zip](http://ledblinky.net/downloads/controls.ini.0.141.1.zip)

<a name="title" />

### MAME title display and sorting support for Attract-Mode: [*updateromlist.py*](updateromlist.py)

Python program to update Attract-Mode MAME romlist with additional game data:

- The *AltTitle* field is replaced by a display title.
- The *Buttons* field is replaced by a sortable title.
- The *Extra* field is replaced by a formatted tag to indicate whether hiscore, benchmark, bezel and/or controls data are available. This can be used to contruct Attract-Mode filters.

<a name="start" />

### MAME startup scripts: [*mame.bash*](mame.bash) and [*mame.csh*](mame.csh)

Startup scripts to automate the execution of [*hiscoreanalysis.py*](hiscoreanalysis.py) and [*benchmarkanalysis.py*](benchmarkanalysis.py) immediately after running a game.

<a name="layout" />

### New Attract-Mode layout with above functionality: [*mylayout*](mylayout)

New Attract-Mode layout which uses the above functionality:

- Current hiscore displayed for each game
- Current benchmark displayed for each game
- Bezel artwork displayed for each game
- Controls information displayed for each game
- Custom display and sorting titles

Requirements:

- **AMhiscores.ini** generated by [*hiscoreanalysis.py*](hiscoreanalysis.py)
- **AMbenchmarks.ini** generated by [*benchmarkanalysis.py*](benchmarkanalysis.py)
- **AMbezels.ini** generated by [*bezelanalysis.py*](bezelanalysis.py)
- **AMcontrols.ini** generated by [*controlanalysis.py*](controlanalysis.py)
- An updated romlist generated by [*updateromlist.py*](updateromlist.py)
