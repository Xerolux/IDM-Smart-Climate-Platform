// Xerolux Ultimate Air B-ES4-AIR enclosure
// Two-piece screw-fastened FDM enclosure for the 130 x 100 mm PCB.
// OpenSCAD: -D 'part="base"', 'part="lid"', 'part="plate"' or 'assembly'.

part = "assembly";
$fn = 48;

case_w = 150;
case_h = 120;
corner_r = 5;
wall = 2.4;
floor_t = 2.4;
base_h = 9;
lid_h = 17.5;
roof_t = 2.4;
fit = 0.30;
board_z = 5.8;
pcb_t = 1.6;

// KiCad holes transformed with enclosure Y = 120 - KiCad Y.
board_holes = [[14,106], [115,85], [14,14], [136,14]];
case_screws = [[5.5,5.5], [144.5,5.5], [5.5,114.5], [144.5,114.5]];

module rounded_rect_2d(w,h,r) {
    hull() for (x=[r,w-r], y=[r,h-r]) translate([x,y]) circle(r=r);
}

module rounded_prism(w,h,z,r) {
    linear_extrude(height=z) rounded_rect_2d(w,h,r);
}

module shell(w,h,z,bottom,thickness,r) {
    difference() {
        rounded_prism(w,h,z,r);
        translate([thickness,thickness,bottom])
            linear_extrude(height=z-bottom+0.2)
                offset(delta=-thickness) rounded_rect_2d(w,h,r);
    }
}

module west_cut(y,width,z0,height)  { translate([-1,y-width/2,z0]) cube([wall+3,width,height]); }
module east_cut(y,width,z0,height)  { translate([case_w-wall-2,y-width/2,z0]) cube([wall+3,width,height]); }
module south_cut(x,width,z0,height) { translate([x-width/2,-1,z0]) cube([width,wall+3,height]); }
module north_cut(x,width,z0,height) { translate([x-width/2,case_h-wall-2,z0]) cube([width,wall+3,height]); }

module connector_side_cuts(z0,height) {
    // J1 IDM, J2 isolated RS-485 and J8 0-10 V push-in terminals.
    west_cut(61.2,25,z0,height);
    east_cut(79.2,25,z0,height);
    east_cut(47.2,16,z0,height);
    // USB-C J3 and optional internal J4 expansion connector.
    south_cut(75,14,z0,height);
    south_cut(88,15,z0,height);
    // J5/J6 1-Wire and J7 two dry-contact inputs.
    north_cut(88.7,19,z0,height);
    north_cut(108.7,19,z0,height);
    north_cut(130.7,19,z0,height);
}

module base_locating_lip() {
    difference() {
        translate([wall+fit,wall+fit,floor_t-0.1])
            linear_extrude(height=base_h+2-floor_t+0.1)
                offset(delta=-(wall+fit)) rounded_rect_2d(case_w,case_h,corner_r);
        translate([wall+fit+1.2,wall+fit+1.2,floor_t-0.2])
            linear_extrude(height=base_h+2.3-floor_t+0.2)
                offset(delta=-(wall+fit+1.2)) rounded_rect_2d(case_w,case_h,corner_r);
    }
}

module base() {
    difference() {
        union() {
            shell(case_w,case_h,base_h,floor_t,wall,corner_r);
            for (p=board_holes)
                translate([p[0],p[1],floor_t-0.1]) cylinder(h=board_z-floor_t+0.1,r=3.5);
            for (p=case_screws)
                translate([p[0],p[1],floor_t-0.1]) cylinder(h=base_h-floor_t+0.1,r=4.2);
            base_locating_lip();
            // Labyrinth baffles below the AIR intake keep fingers away from U8-U10.
            for (x=[21,35,49]) translate([x,4.2,floor_t]) cube([1.6,20,4.2]);
        }
        for (p=board_holes)
            translate([p[0],p[1],floor_t-0.1]) cylinder(h=board_z-floor_t+0.3,r=1.05);
        for (p=case_screws) {
            translate([p[0],p[1],base_h-5.3]) cylinder(h=5.5,r=1.95);
            translate([p[0],p[1],base_h-0.7]) cylinder(h=0.9,r1=1.95,r2=2.2);
        }
        // Two recessed wall-mount holes.
        for (x=[42,108]) {
            translate([x,60,-0.1]) cylinder(h=floor_t+0.2,r=2.1);
            translate([x,60,-0.1]) cylinder(h=1.45,r1=4.2,r2=2.1);
        }
        connector_side_cuts(board_z-1.1,base_h+3-(board_z-1.1));
        // Low side intake for SCD41/SGP41/BMP390 sensor island.
        for (x=[17:6:53]) south_cut(x,3.0,3.0,3.0);
    }
}

module lid_access_openings() {
    // Tool-free push-in wiring access.
    translate([79.5,100,lid_h-roof_t-0.1]) cube([18.5,12,roof_t+0.3]);
    translate([99.5,100,lid_h-roof_t-0.1]) cube([18.5,12,roof_t+0.3]);
    translate([121.5,100,lid_h-roof_t-0.1]) cube([18.5,12,roof_t+0.3]);
    translate([10,49,lid_h-roof_t-0.1]) cube([12,25,roof_t+0.3]);
    translate([128,67,lid_h-roof_t-0.1]) cube([12,25,roof_t+0.3]);
    translate([128,40,lid_h-roof_t-0.1]) cube([12,15,roof_t+0.3]);

    // Reset, boot and service buttons; three diagnostic LEDs; termination switch.
    for (p=[[70,77],[77,77],[108,15]])
        translate([p[0],p[1],lid_h-roof_t-0.1]) cylinder(h=roof_t+0.3,r=2.5);
    for (p=[[82,80],[95,80],[104,80]])
        translate([p[0],p[1],lid_h-roof_t-0.1]) cylinder(h=roof_t+0.3,r=1.5);
    translate([118.5,51,lid_h-roof_t-0.1]) cube([7,12,roof_t+0.3]);

    // SHT45 ventilation at the thermally separated upper sensor position.
    for (x=[67:4:83]) translate([x,92,lid_h-roof_t-0.1]) cube([2,14,roof_t+0.3]);
    // Large low-resistance AIR exchange area over CO2/VOC/NOx/pressure sensors.
    for (x=[18:4:54]) translate([x,8,lid_h-roof_t-0.1]) cube([2,25,roof_t+0.3]);
    // Air exchange around the local KTY reference sensor.
    for (y=[68:4:80]) translate([20,y,lid_h-roof_t-0.1]) cube([14,2,roof_t+0.3]);
}

module lid_labels() {
    translate([75,64,lid_h-0.08]) linear_extrude(height=0.53)
        text("XEROLUX  ULTIMATE AIR",size=5,halign="center",valign="center");
    translate([75,57,lid_h-0.08]) linear_extrude(height=0.53)
        text("B-ES4-AIR | xerolux.de | 2026",size=3.0,halign="center",valign="center");
    translate([36,37,lid_h-0.08]) linear_extrude(height=0.53)
        text("CO2  VOC  NOx  hPa",size=2.5,halign="center",valign="center");
}

module lid() {
    difference() {
        union() {
            shell(case_w,case_h,lid_h,lid_h-roof_t,wall,corner_r);
            for (p=case_screws) translate([p[0],p[1],0]) cylinder(h=lid_h-roof_t+0.1,r=4.2);
            lid_labels();
        }
        for (p=case_screws) {
            translate([p[0],p[1],-0.1]) cylinder(h=lid_h+0.8,r=1.7);
            translate([p[0],p[1],lid_h-2.2]) cylinder(h=2.4,r1=1.7,r2=3.25);
        }
        connector_side_cuts(-0.1,11.5);
        lid_access_openings();
    }
}

module preview_board() {
    color("SeaGreen",0.82) translate([10,10,board_z]) cube([130,100,pcb_t]);
    color("LimeGreen",0.9) {
        translate([10.5,50.5,board_z+pcb_t]) cube([9.2,21.6,14.4]);
        translate([130.5,68.5,board_z+pcb_t]) cube([9.2,21.6,14.4]);
        translate([80.5,100.5,board_z+pcb_t]) cube([16.6,9.2,14.4]);
        translate([100.5,100.5,board_z+pcb_t]) cube([16.6,9.2,14.4]);
        translate([122.5,100.5,board_z+pcb_t]) cube([16.6,9.2,14.4]);
        translate([130.5,41.5,board_z+pcb_t]) cube([9.2,11.6,14.4]);
    }
    color("Silver",0.95) translate([69.7,9.2,board_z+pcb_t]) cube([10.7,5.8,3.6]);
    color("CornflowerBlue",0.9) translate([18,10,board_z+pcb_t]) cube([37,12,10.2]);
}

if (part == "base") base();
else if (part == "lid") lid();
else if (part == "plate") {
    // 310 x 120 mm plus 5 mm brim fits the Ultimaker S5 330 x 240 mm bed.
    translate([-155,-60,0]) { base(); translate([160,0,0]) lid(); }
}
else {
    color("DimGray") base();
    preview_board();
    color("Gainsboro",0.72) translate([0,0,base_h+0.2]) lid();
}
