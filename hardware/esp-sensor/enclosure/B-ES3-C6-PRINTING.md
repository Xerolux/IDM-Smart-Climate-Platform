# B-ES3-C6 enclosure printing and assembly

The enclosure fits the 130 x 80 mm B-ES3-C6 PCB. Its outside dimensions are
150 x 100 x approximately 26.5 mm when assembled. The base and lid are separate
manifold STL parts and are designed to print with their open sides facing up.

## Recommended print settings

- PETG or ASA; PLA is suitable only for dry, temperature-controlled rooms
- 0.20 mm layer height, 0.4 mm nozzle
- four perimeters, five top/bottom layers, 25% gyroid infill
- no supports expected; enable a 5 mm brim for ASA if needed
- compensate first-layer elephant foot so the locating lip remains free

## Hardware

- 4 x M3 x 25 mm countersunk screws for the lid
- 4 x M3 heat-set inserts, approximately 4.0-4.2 mm OD and 5 mm long
- 4 x M2.5 x 6 mm thread-forming plastic screws for the PCB
- optional 2 x wall screws up to 4 mm shank diameter

Install the M3 inserts from the top of the four base corner bosses. The PCB is
then placed on its four dedicated supports and fixed separately. Route and test
all field wiring before closing the lid.

## Openings

The model provides side and top access for J1/J2/J5-J8, USB-C J3, click
connector J4, SW3 termination, reset/boot/service buttons and all three LEDs.
Separate ventilation fields sit above the SHT45 and local temperature sensor.

The first print remains a mechanical engineering sample: verify connector
reach, button access, insert fit and component height before producing a larger
batch. Adjust `fit` in the SCAD source by 0.1-0.2 mm if the printer is unusually
tight or loose.
