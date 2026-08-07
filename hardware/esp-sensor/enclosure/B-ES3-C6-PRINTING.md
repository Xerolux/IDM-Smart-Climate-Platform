# B-ES3-C6 enclosure printing and assembly

The enclosure fits the 130 x 80 mm B-ES3-C6 PCB. Its outside dimensions are
150 x 100 x approximately 26.5 mm when assembled. The base and lid are separate
manifold STL parts and are designed to print with their open sides facing up.

## UltiMaker S5: prepared production sample

The supplied S5 print plate and G-code place both parts on one build plate. The
G-code was sliced with CuraEngine 5.11.0 specifically for an UltiMaker S5 with
an AA 0.4 print core and UltiMaker PLA:

- 0.20 mm layer height
- four walls, six top and six bottom layers
- 25% gyroid infill
- 5 mm brim with 0.1 mm gap
- no supports
- 200 degrees C nozzle, 60 degrees C build plate
- estimated 15 h 09 min and approximately 154 g PLA

Use the supplied G-code only with that exact machine, print core and material.
For PETG, ASA, another PLA or another nozzle, import the STL plate and re-slice
with the appropriate material profile. PETG is preferred for warm technical
rooms; PLA is suitable for the first fit sample and normal dry indoor rooms.
Compensate first-layer elephant foot if the locating lip is unusually tight.

## Hardware

- 4 x M3 x 25 mm countersunk screws for the lid
- 4 x M3 heat-set inserts, approximately 4.0-4.2 mm OD and 5 mm long; the
  printed pilot is 3.9 mm with a 4.4 mm lead-in
- 4 x M2.5 x 6 mm thread-forming plastic screws for the PCB
- optional 2 x wall screws up to 4 mm shank diameter

Install the M3 inserts from the top of the four base corner bosses. The PCB is
then placed on its four dedicated supports and fixed separately. Route and test
all field wiring before closing the lid.

## Openings

The model provides side and top access for J1/J2/J5-J8, USB-C J3, click
connector J4, SW3 termination, reset/boot/service buttons and all three LEDs.
Separate ventilation fields sit above the SHT45 and local temperature sensor.
The small reset, boot and service openings are tool/paper-clip access holes,
not finger-operated plungers.

The 14.4 mm-high MX205R terminal body was checked against 16.7 mm internal
clearance above the PCB, leaving approximately 2.3 mm to the roof. The S5 plate
occupies 310 x 100 mm before its brim and fits the S5's 330 x 240 mm build area.

The first print remains a mechanical engineering sample: verify connector
reach, button access, insert fit and component height before producing a larger
batch. Adjust `fit` in the SCAD source by 0.1-0.2 mm if the printer is unusually
tight or loose.
