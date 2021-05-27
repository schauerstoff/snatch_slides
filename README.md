# snatch_slides

This script automates the tiring process skipping through the lecture and taking a screenshot everytime a new slide appears.
If a slide is 'new' is determined by simple image processing: Save preceding slide, take a new screenshot, subtract the images. 
Then sum all the absolute values of these differences and compare them to a threshold. The more different the images are, the bigger the sum will be.
For the set resolution, 1.000.000 seems to work.
[Save two previous slides if there is a lot of skipping back and forth in your lecture.]

By default, this script will work for Panopto player, but one should be able to use it with any sort of player as long as the CSS IDs for
the buttons (play, mute, ...) are set correctly in the beginning.

How to use:
1. Install Python 3
2. Install all required packages via PIP
3. Download chromedriver corresponding to chrome version
	and set path for chromedriver
4. Set CSS IDs if not using Panopto
5. Set link to video of lecture


Troubleshooting:
If screenshots don't fully capture what's shown on screen:
- Einstellungen > System > Anzeige > Skalierung und Anordnung: Groesse von Text und ...: 100% instead of 125%

Do not touch the browser window after the first screenshot is taken. Screenshots need the have the same resolution to be comparable.
Change resolution in Browser constructor.
- ValueError: operands could not be broadcast together with shapes (502,892) (880,1564)
