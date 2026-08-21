import cadquery as cq
import math

# array

columns = 6
rows = 4

# cups
cavity_diam  = 40.0
cup2cup      = 45
total_length = 300
total_width  = 200

depth  = 20
floor  = 2              
height = floor + depth

# star shape
star_r             = 12.0   # outer radius of the star
star_inner_ratio   = 0.42   # inner/outer radius -> star sharpness
star_outline_scale = 0.82   # inner star as fraction of outer -> outline thickness

# XY planes
top_z    = height / 2.0
floor_z  = top_z - depth
bottom_z = -height / 2.0

# feature sizes
structure_fillet = 10
tray_thk         = 2.0
tray_lip         = 12.0

# star helper
def star_points(r, ratio=star_inner_ratio, n=5, rot=math.pi / 2.0):
    pts = []
    for i in range(2 * n):
        ang = rot + i * math.pi / n
        rad = r if i % 2 == 0 else r * ratio
        pts.append((rad * math.cos(ang), rad * math.sin(ang)))
    return pts

### structure

structure = (
    cq.Workplane("XY")
    .box(total_length, total_width, height)
    .edges("|Z").fillet(structure_fillet)
    .faces("-Z").shell(-floor)
)
structure_cut = (
    cq.Workplane("XY")
    .rarray(cup2cup, cup2cup, columns, rows, True)
    .cylinder(height * 3, cavity_diam / 2.0, (0, 0, 1))
)

structure = structure.cut(structure_cut)

### tray

tray = (
    cq.Workplane("XY", origin=(0, 0, bottom_z + tray_thk / 2.0))
    .box(total_length + 2 * tray_lip, total_width + 2 * tray_lip, tray_thk)
    .edges("|Z").fillet(5)
)

tray_cut = (
    cq.Workplane("XY", origin=(0,0,-5))
    .box(total_length - 0.5, total_width - 0.5, height -5)
    .edges("|Z").fillet(structure_fillet)
)

tray = tray.cut(tray_cut)

solid  = tray.union(structure)

solid = (solid
    .faces("+Z").faces("<Z")                    # pick up face -> pick lowest face
    .wires(cq.selectors.AreaNthSelector(0))     # the junction
    .fillet(2.5)
    .edges("#Z")
    .fillet(0.35)
)

#### form

form = (
    cq.Workplane("XY")
    .cylinder(height, cavity_diam / 2.0, (0, 0, 1))
    .faces("+Z").shell(-floor)
    .faces("<Z").edges().fillet(0.35)
    .faces("+Z").faces("<Z").edges().fillet(0.35)
)

forms = (
    cq.Workplane("XY")
    .rarray(cup2cup, cup2cup, columns, rows, True)
    .eachpoint(form, combine=False)
)

solid = forms.union(solid)

#stars

star = (
    cq.Workplane("XY", origin=(0, 0, floor_z))
    .polyline(star_points(star_r)).close()
    .polyline(star_points(star_r * star_outline_scale)).close()
    .extrude(2)

)

stars = (
    cq.Workplane("XY", origin=(0, 0, 0))
    .rarray(cup2cup, cup2cup, columns, rows, True)
    .eachpoint(star, combine=False)
)

solid = solid.union(stars)

show_object(solid)