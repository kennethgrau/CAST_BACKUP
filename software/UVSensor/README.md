# CAST Software - UV Sensor

This contains all the software used on our Capstone Team's UV Sensor. When the UV lights reaches a certain threshold on the sensor, the Ardiuno will flash a green light. In the scenario where the UV lights has not reached the threshold, the RGB will stay red.

## Data to Support values used in Code

Below shows two different documentations that provide the evidence for data used in the code.

[Gidari-2021-Sars-cov--survival-on-surfaces-and-.pdf](https://github.com/CAST2022/CAST/files/8485068/Gidari-2021-Sars-cov--survival-on-surfaces-and-.pdf)

The document above states "Based on our results, a smaller dose of UV-C (10.25–23.71 mJ/cm2) is enough to reduce the viral titer of >99.99%." Meaning 23.71 mJ/cm2 would cover every type of surface covid may appear on.
If a user knows the specific type of surface the sensor will be placed on, the value can be changed to reflect that type of surface.

Simply change **UVDoseRequirement** value to reflect the type of surface you plan on putting the sensor on.

https://cdn-shop.adafruit.com/datasheets/1918guva.pdf

The specifications sheet above shows the conversions needed to get the input converted to UV intensity.

## Sensor Data

The following file shows the UV sensor data from a panel of 5 UV-C LEDs in the 265 nm range.

[UV.Sensor.Test.Values.docx](https://github.com/CAST2022/CAST/files/8485109/UV.Sensor.Test.Values.docx)


## Code Information
You can plug in the BKI into your serial port and the code will print the UV intensity to your terminal. 
