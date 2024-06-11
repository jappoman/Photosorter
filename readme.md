# Photosorter

## Description
Photosorter allows you to sort your pictures by events, which means moments that are far away in space and time from each others.

It works by scanning GPS metadata and shooting time of all files (this is done for scanning various images and video file types) in a specific folder and all the subfolders. Furthermore, the more you get far away from a specific home point, the more pictures spreaded in space and time are put together.
This is designed to recognise for example a dinner out (short and near) against a holiday trip (longer and farther).

The folder created are named `Event000X` followed by (when present) the address of the shooting place and the date of the event (yyyy-mm-dd).
If you want to simplify the address of the events you can write up a little dictionary that will subsitute the long address with a more familiar one (eg: `Verdi street n.1` with `Home`).

You can edit every space and time parameter to suite better your needs and then save them to a config file to load them later.


## Special funcions

- **Create known places dictionary only:** if you check this you will output a "places_to_replace.txt" file which contains all the unique address found in all the pictures. Fill this file with more familiar names after the "=" symbol and use it to have prettier name on the second run.

- **Move files instead of copy (faster!)**: if you check this you will move the files instead of copying them. This process is way faster.
