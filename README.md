# MAME support tools for Attract-Mode

This repository contains a collection of programs that provides [MAME](http://www.mamedev.org/) support for the [Attract-Mode](http://www.attractmode.org/) frontend:

- [MAME hiscore support for Attract-Mode](#hiscore) ([*hiscoreanalysis.py*](hiscoreanalysis.py))
- MAME bezel art support for Attract-Mode (*bezelanalysis.py*)
- MAME controls support for Attract-Mode (*controlanalysis.py*)
- MAME benchmark support for Attract-Mode ([*benchmarkgenerator.py*](benchmarkgenerator.py) and [*benchmarkanalysis.py*](benchmarkanalysis.py))
- MAME title display and sorting support for Attract-Mode ([*updateromlist.py*](updateromlist.py))
- MAME startup scripts ([*mame.bash*](mame.bash) and [*mame.csh*](mame.csh))
- New Attract-Mode layout with above functionality (*layout.nut*)

<a name="hiscore" />
## MAME hiscore support for Attract-Mode ([*hiscoreanalysis.py*](hiscoreanalysis.py))

Python program to get hiscores from MAME games using the 'hi2txt' Java archive (see http://greatstone.free.fr/hi2txt/), 
and save them in formatted .ini files in a dedicated Attract-Mode hiscores directory. This allows hiscores to be 
displayed in any Attract-Mode layout using the 'file-format' module.

Requirements:

- hi2txt.jar and hi2txt.zip (see http://greatstone.free.fr/hi2txt/)
- Java (see https://www.java.com)
- hiscore.dat (see http://highscore.mameworld.info/)
