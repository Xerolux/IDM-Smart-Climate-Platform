// Xerolux B-ES5-MODULAR enclosure for 130 x 100 mm base plus AIR-SLOT modules.
part="assembly"; $fn=48;
case_w=150; case_h=120; r=5; wall=2.4; floor_t=2.4; base_h=9;
lid_h=22.5; roof_t=2.4; fit=.30; board_z=5.8; pcb_t=1.6;
holes=[[14,106],[115,85],[14,14],[136,14]];
screws=[[5.5,5.5],[144.5,5.5],[5.5,114.5],[144.5,114.5]];

module rr2(w,h,rad) { hull() for(x=[rad,w-rad],y=[rad,h-rad]) translate([x,y]) circle(rad); }
module prism(w,h,z,rad) { linear_extrude(z) rr2(w,h,rad); }
module shell(z,bottom) { difference(){ prism(case_w,case_h,z,r); translate([wall,wall,bottom]) linear_extrude(z-bottom+.2) offset(delta=-wall) rr2(case_w,case_h,r); } }
module west(y,w,z,h)  { translate([-1,y-w/2,z]) cube([wall+3,w,h]); }
module east(y,w,z,h)  { translate([case_w-wall-2,y-w/2,z]) cube([wall+3,w,h]); }
module south(x,w,z,h) { translate([x-w/2,-1,z]) cube([w,wall+3,h]); }
module north(x,w,z,h) { translate([x-w/2,case_h-wall-2,z]) cube([w,wall+3,h]); }

module connector_cuts(z,h) {
  west(61.2,25,z,h);             // J1 IDM
  east(79.2,25,z,h);             // J2 RS-485
  east(47.2,16,z,h);             // J8 0-10 V input
  south(103,14,z,h);             // J3 USB-C
  south(119,15,z,h);             // J4 expansion
  north(88.7,19,z,h); north(108.7,19,z,h); north(130.7,19,z,h);
}

module lip(){ difference(){
  translate([wall+fit,wall+fit,floor_t-.1]) linear_extrude(base_h+2-floor_t+.1) offset(delta=-(wall+fit)) rr2(case_w,case_h,r);
  translate([wall+fit+1.2,wall+fit+1.2,floor_t-.2]) linear_extrude(base_h+2.3-floor_t+.2) offset(delta=-(wall+fit+1.2)) rr2(case_w,case_h,r);
} }

module base(){ difference(){ union(){
  shell(base_h,floor_t); lip();
  for(p=holes) translate([p[0],p[1],floor_t-.1]) cylinder(h=board_z-floor_t+.1,r=3.5);
  for(p=screws) translate([p[0],p[1],floor_t-.1]) cylinder(h=base_h-floor_t+.1,r=4.2);
 }
 for(p=holes) translate([p[0],p[1],floor_t-.1]) cylinder(h=board_z-floor_t+.3,r=1.05);
 for(p=screws){ translate([p[0],p[1],base_h-5.3]) cylinder(h=5.5,r=1.95); translate([p[0],p[1],base_h-.7]) cylinder(h=.9,r1=1.95,r2=2.2); }
 for(x=[42,108]){ translate([x,60,-.1]) cylinder(h=floor_t+.2,r=2.1); translate([x,60,-.1]) cylinder(h=1.45,r1=4.2,r2=2.1); }
 connector_cuts(board_z-1.1,base_h+3-(board_z-1.1));
 for(x=[14:6:94]) south(x,3,3,3); // low module air intake
} }

module roof_openings(){
 // Push-in terminals.
 translate([79.5,100,lid_h-roof_t-.1]) cube([18.5,12,roof_t+.3]);
 translate([99.5,100,lid_h-roof_t-.1]) cube([18.5,12,roof_t+.3]);
 translate([121.5,100,lid_h-roof_t-.1]) cube([18.5,12,roof_t+.3]);
 translate([10,49,lid_h-roof_t-.1]) cube([12,25,roof_t+.3]);
 translate([128,67,lid_h-roof_t-.1]) cube([12,25,roof_t+.3]);
 translate([128,40,lid_h-roof_t-.1]) cube([12,15,roof_t+.3]);
 // Buttons, LEDs and RS-485 termination switch.
  for(p=[[70,77],[77,77],[116,24]]) translate([p[0],p[1],lid_h-roof_t-.1]) cylinder(h=roof_t+.3,r=2.5);
 for(p=[[82,80],[95,80],[104,80]]) translate([p[0],p[1],lid_h-roof_t-.1]) cylinder(h=roof_t+.3,r=1.5);
 translate([118.5,51,lid_h-roof_t-.1]) cube([7,12,roof_t+.3]);
 // SHT45 and broad AIR-SLOT exchange area.
 for(x=[67:4:83]) translate([x,92,lid_h-roof_t-.1]) cube([2,14,roof_t+.3]);
 for(x=[14:4:94]) translate([x,12,lid_h-roof_t-.1]) cube([2,30,roof_t+.3]);
 for(y=[68:4:80]) translate([20,y,lid_h-roof_t-.1]) cube([14,2,roof_t+.3]);
}

module labels(){
 translate([75,65,lid_h-.08]) linear_extrude(.53) text("XEROLUX  MODULAR AIR",5,halign="center",valign="center");
 translate([75,58,lid_h-.08]) linear_extrude(.53) text("B-ES5-MODULAR | xerolux.de | 2026",2.8,halign="center",valign="center");
 translate([54,45,lid_h-.08]) linear_extrude(.53) text("CO2      VOC/NOx      PRESSURE",2.4,halign="center",valign="center");
}

module retainers(){
 // Low internal rails limit module lift without touching sensor packages.
 for(x=[12.0,38.0,40.0,66.0,68.0,94.0]) translate([x,14,lid_h-roof_t-4.0]) cube([1.2,28,2.0]);
}

module lid(){ difference(){ union(){ shell(lid_h,lid_h-roof_t); for(p=screws) translate([p[0],p[1],0]) cylinder(h=lid_h-roof_t+.1,r=4.2); labels(); retainers(); }
 for(p=screws){ translate([p[0],p[1],-.1]) cylinder(h=lid_h+.8,r=1.7); translate([p[0],p[1],lid_h-2.2]) cylinder(h=2.4,r1=1.7,r2=3.25); }
 connector_cuts(-.1,11.5); roof_openings();
} }

module preview(){
 color("SeaGreen",.82) translate([10,10,board_z]) cube([130,100,pcb_t]);
 // Intended 180-degree orientation: three 25 x 25 mm modules over the base PCB.
 for(x=[12.5,40.5,68.5]) color("DarkSeaGreen",.9) translate([x,14.38,board_z+pcb_t+8.5]) cube([25,25,1.6]);
 color("LightSkyBlue",.9) translate([15,17,board_z+pcb_t+10.1]) cube([10.1,10.1,6.5]);
}

if(part=="base") base();
else if(part=="lid") lid();
else if(part=="plate") translate([-155,-60,0]){ base(); translate([160,0,0]) lid(); }
else { color("DimGray") base(); preview(); color("Gainsboro",.7) translate([0,0,base_h+.2]) lid(); }
