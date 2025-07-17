# ComponentLabels

This script generates labels for zip bags with all sorts of electronic or mechanical components.

It is primarily meant for [these](https://www.obalyvysocina.cz/produkty/samolepici-etikety) labels (70x25.4 mm) and [these](https://www.obalyvysocina.cz/produkty/rychlouzaviraci-sacek-extra-pevny#rychlouzaviraci-sacek-silny8x12) 8x12 cm zip bags. However, the generator script also supports AVERY 5260 or AVERY L7157 labels.

![Some examples of ComponentLabels](https://github.com/user-attachments/assets/97d1cfc7-5ef2-4d29-b490-5f422465625b)

## Supported components

- Resistors (resistance, 3 & 4 digit SMD code, EIA-96 code and 3 & 4 band color codes)
- Capacitors (capacitance, 3 digit SMD code, EIA-198 code and 3 band color code (yes, those appear to actually exist))
- Diodes & Schottky diodes (name, forward voltage/current, reverse voltage)
- Zener diodes (name, reverse voltage/current, forward voltage)
- LEDs (diameter/name, forward voltage/current, wavelength)
- PNP/NPN BJT (name, base-emittor voltage, collector-emittor voltage/current)
- P/N-channel MOSFET (name, gate-source voltage, drain current, drain-source voltage)
- Square/Hexagonal nuts (thread type, thickness, width and diameter)
- Washers (thread type, thickness, diameter)
- Recessed/Round-head/Flat-head screws (thread type, head width, head height and screw length)
- Threaded inserts for 3D prints (thread type, diameter and length)
- Compression/Extension springs (diameter and length)

# Usage

- Install python3
- Install the python3 library `reportlab`. This library is used to do the actual PDF generation.
- Add your own required resistor values in `main()` of `LabelGenerator.py`.
- If using Avery L7157 or 5260, change the `layout` value in `main()` to `AVERY_L7157` or `AVERY_5260`.
- Run the script `LabelGenerator.py`!

It will now generate a `ResistorLabels.pdf` that can be used to print onto AVERY 5260/L7157.

# Development

Development dependencies are defined in `requirements-dev.txt`

## Label Alignment Helper Script

`scripts/check_alignment.py` can be used during the development of new label definitions by merging a scanned copy of the labels with the generated PDF.

For example: `./scripts/check_alignment.py --template scanned_labels.pdf --labels ComponentLabels.pdf --output combined.pdf` will produce a file named `combined.pdf` that will have the scanned labels as a background for each page and the generated labels overlayed.

# More Details

This is forked from https://github.com/securelyfitz/ResistorLabels, which is in turn a fork of https://github.com/Finomnis/ResistorLabels

The original is based on an idea from Zach Poff. I liked the design of securelyfitz's forked labels, I just needed to implement more than resistors.

For more details on how to use these labels, visit Zach's website:

https://www.zachpoff.com/resources/quick-easy-and-cheap-resistor-storage/
