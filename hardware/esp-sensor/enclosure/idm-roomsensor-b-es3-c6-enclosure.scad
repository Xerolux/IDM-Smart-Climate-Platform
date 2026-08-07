// Xerolux Smart Climate Sensor B-ES3-C6 enclosure
// Two-piece, screw-fastened FDM enclosure for the 130 x 80 mm PCB.
// Export with: openscad -D 'part="base"' -o ..._base.stl this_file.scad
//              openscad -D 'part="lid"'  -o ..._lid.stl  this_file.scad

part = "assembly";             // "base", "lid", "plate", or "assembly"
$fn = 48;

case_w = 150;
case_h = 100;
corner_r = 5;
wall = 2.4;
floor_t = 2.4;
base_h = 9;
lid_h = 17.5;
roof_t = 2.4;
fit = 0.30;

board_w = 130;
board_h = 80;
board_x = 10;
board_y = 10;
board_z = 5.8;
pcb_t = 1.6;

// KiCad PCB holes transformed into enclosure coordinates.
board_holes = [[14,86], [115,65], [14,14], [136,14]];
case_screws = [[5.5,5.5], [144.5,5.5], [5.5,94.5], [144.5,94.5]];

module rounded_rect_2d(w, h, r) {
    hull()
        for (x = [r, w-r], y = [r, h-r])
            translate([x,y]) circle(r=r);
}

module rounded_prism(w, h, z, r) {
    linear_extrude(height=z) rounded_rect_2d(w,h,r);
}

module shell(w, h, z, bottom, thickness, r) {
    difference() {
        rounded_prism(w,h,z,r);
        translate([thickness,thickness,bottom])
            linear_extrude(height=z-bottom+0.2)
                offset(delta=-thickness)
                    rounded_rect_2d(w,h,r);
    }
}

module west_cut(y, width, z0, height) {
    translate([-1,y-width/2,z0]) cube([wall+3,width,height]);
}

module east_cut(y, width, z0, height) {
    translate([case_w-wall-2,y-width/2,z0]) cube([wall+3,width,height]);
}

module south_cut(x, width, z0, height) {
    translate([x-width/2,-1,z0]) cube([width,wall+3,height]);
}

module north_cut(x, width, z0, height) {
    translate([x-width/2,case_h-wall-2,z0]) cube([width,wall+3,height]);
}

module connector_side_cuts(z0, height) {
    // J1 IDM, J2 RS-485 and J8 0-10 V.
    west_cut(41.2,25,z0,height);
    east_cut(59.2,25,z0,height);
    east_cut(27.2,16,z0,height);

    // USB-C J3 and internal click connector J4.
    south_cut(75,14,z0,height);
    south_cut(88,15,z0,height);

    // J5/J6 1-Wire and J7 dry-contact push-in terminals.
    north_cut(88.7,19,z0,height);
    north_cut(108.7,19,z0,height);
    north_cut(130.7,19,z0,height);
}

module base_locating_lip() {
    // Full-height inner liner is supported by the floor and enters the lid by
    // 2 mm. The 0.30 mm radial fit is suitable for an S5 with a 0.4 mm core.
    difference() {
        translate([wall+fit,wall+fit,floor_t-0.1])
            linear_extrude(height=base_h+2.0-floor_t+0.1)
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

            // PCB supports. The 2.1 mm pilot accepts M2.5 thread-forming screws.
            for (p=board_holes)
                translate([p[0],p[1],floor_t-0.1]) cylinder(h=board_z-floor_t+0.1,r=3.5);

            // Lid screw bosses for M3 heat-set inserts (4.2 mm nominal OD).
            for (p=case_screws)
                translate([p[0],p[1],floor_t-0.1]) cylinder(h=base_h-floor_t+0.1,r=4.2);

            base_locating_lip();
        }

        for (p=board_holes)
            translate([p[0],p[1],floor_t-0.1]) cylinder(h=board_z-floor_t+0.3,r=1.05);

        for (p=case_screws) {
            translate([p[0],p[1],base_h-5.3]) cylinder(h=5.5,r=1.95);
            translate([p[0],p[1],base_h-0.7]) cylinder(h=0.9,r1=1.95,r2=2.2);
        }

        // Wall-mounting holes with recessed screw heads on the outside.
        for (x=[42,108]) {
            translate([x,50,-0.1]) cylinder(h=floor_t+0.2,r=2.1);
            translate([x,50,-0.1]) cylinder(h=1.45,r1=4.2,r2=2.1);
        }

        connector_side_cuts(board_z-1.1,base_h+3.0-(board_z-1.1));
    }
}

module lid_access_openings() {
    // Direct top access to every push-in terminal.
    translate([79.5,80.0,lid_h-roof_t-0.1]) cube([18.5,12.0,roof_t+0.3]);
    translate([99.5,80.0,lid_h-roof_t-0.1]) cube([18.5,12.0,roof_t+0.3]);
    translate([121.5,80.0,lid_h-roof_t-0.1]) cube([18.5,12.0,roof_t+0.3]);
    translate([10.0,29.0,lid_h-roof_t-0.1]) cube([12.0,25.0,roof_t+0.3]);
    translate([128.0,47.0,lid_h-roof_t-0.1]) cube([12.0,25.0,roof_t+0.3]);
    translate([128.0,20.0,lid_h-roof_t-0.1]) cube([12.0,15.0,roof_t+0.3]);

    // Reset, boot and service buttons.
    for (p=[[70,57],[77,57],[108,15]])
        translate([p[0],p[1],lid_h-roof_t-0.1]) cylinder(h=roof_t+0.3,r=2.5);

    // Status and diagnostic LED windows.
    for (p=[[82,60],[95,60],[104,60]])
        translate([p[0],p[1],lid_h-roof_t-0.1]) cylinder(h=roof_t+0.3,r=1.5);

    // Slide-switch access for RS-485 termination.
    translate([118.5,31.0,lid_h-roof_t-0.1]) cube([7.0,12.0,roof_t+0.3]);

    // SHT45 ventilation: short slots avoid a straight finger/tool path.
    for (x=[67:4:83])
        translate([x,72,lid_h-roof_t-0.1]) cube([2.0,14.0,roof_t+0.3]);

    // Additional airflow around the local temperature sensor.
    for (y=[48:4:60])
        translate([20,y,lid_h-roof_t-0.1]) cube([14.0,2.0,roof_t+0.3]);
}

module lid_labels() {
    translate([75,47,lid_h-0.08])
        linear_extrude(height=0.53)
            text("XEROLUX  B-ES3-C6",size=5,halign="center",valign="center");
    translate([75,40,lid_h-0.08])
        linear_extrude(height=0.53)
            text("xerolux.de  |  2026",size=3.2,halign="center",valign="center");
    translate([108,10,lid_h-0.08])
        linear_extrude(height=0.53)
            text("SERVICE",size=2.5,halign="center",valign="center");
}

module lid() {
    difference() {
        union() {
            shell(case_w,case_h,lid_h,lid_h-roof_t,wall,corner_r);

            // Continuous screw tubes prevent the lid from bowing.
            for (p=case_screws)
                translate([p[0],p[1],0]) cylinder(h=lid_h-roof_t+0.1,r=4.2);
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
    // Non-exported fit-check model derived from the KiCad coordinates.
    color("SeaGreen",0.82)
        translate([board_x,board_y,board_z]) cube([board_w,board_h,pcb_t]);

    // Push-in terminal envelopes: J1, J2, J5, J6, J7 and J8.
    // The 14.4 mm height comes from the MX205R-5.0 datasheet and is used
    // here as the worst-case roof-clearance check (16.7 mm are available).
    color("LimeGreen",0.9) {
        translate([10.5,30.5,board_z+pcb_t]) cube([9.2,21.6,14.4]);
        translate([130.5,48.5,board_z+pcb_t]) cube([9.2,21.6,14.4]);
        translate([80.5,80.5,board_z+pcb_t]) cube([16.6,9.2,14.4]);
        translate([100.5,80.5,board_z+pcb_t]) cube([16.6,9.2,14.4]);
        translate([122.5,80.5,board_z+pcb_t]) cube([16.6,9.2,14.4]);
        translate([130.5,21.5,board_z+pcb_t]) cube([9.2,11.6,14.4]);
    }

    // USB-C and click connector envelopes.
    color("Silver",0.95) {
        translate([69.7,9.2,board_z+pcb_t]) cube([10.7,5.8,3.6]);
        translate([82.1,10.0,board_z+pcb_t]) cube([11.9,7.0,5.0]);
    }
}

if (part == "base") base();
else if (part == "lid") lid();
else if (part == "plate") {
    // S5 build-plate layout centered at the STL origin. Cura places that
    // origin at the 330 x 240 mm bed center, leaving 10 mm X margin.
    translate([-155,-50,0]) {
        base();
        translate([160,0,0]) lid();
    }
}
else {
    color("DimGray") base();
    preview_board();
    color("Gainsboro",0.72) translate([0,0,base_h+0.2]) lid();
}
