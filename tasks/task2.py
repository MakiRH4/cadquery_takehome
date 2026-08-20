import cadquery as cq
import math

cols = 6          # number of cavities wide  (X)
rows = 4          # number of cavities long  (Y)

cavity_diam = 40.0

#
# Proportions -- all expressed as a fraction of the anchor, Lego-style
#
clearance          = 0.1
wall_scale         = 0.18     # material between neighbouring cavities
depth_scale        = 0.35     # how deep each pocket is
floor_scale        = 0.12     # solid floor left under each pocket
border_scale       = 0.25     # margin from outer cavity edge to tray edge
rim_w_scale        = 0.14     # width of the raised perimeter rim
rim_h_scale        = 0.06     # how tall the rim stands above the field
corner_fillet_scale= 0.10     # vertical corner rounding
base_fillet_scale  = 0.03     # bottom-edge rounding
star_r_scale       = 0.30     # outer radius of the star
star_h_scale       = 0.045    # how far the star stands off the pocket floor
star_inner_ratio   = 0.42     # inner/outer radius -> star sharpness
star_outline_scale = 0.82     # inner star as fraction of outer -> outline thickness
notch_w_scale      = 0.22     # width of the alignment notches in the rim
notches_per_side   = 2

#
# Derived (dynamic) dimensions
#
wall   = cavity_diam * wall_scale
pitch  = cavity_diam + wall                       # centre-to-centre spacing
depth  = 10#cavity_diam * depth_scale
floor  = 2#cavity_diam * floor_scale
border = cavity_diam * border_scale
rim_w  = cavity_diam * rim_w_scale
rim_h  = cavity_diam * rim_h_scale
star_r = cavity_diam * star_r_scale
star_h = cavity_diam * star_h_scale
notch_w= cavity_diam * notch_w_scale

height = floor + depth                             # base thickness
total_length = (cols - 1) * pitch + cavity_diam + 2 * border - 2 * clearance
total_width  = (rows - 1) * pitch + cavity_diam + 2 * border - 2 * clearance

top_z   = height / 2.0                              # field level (top of base box)
floor_z = top_z - depth                             # pocket-floor level


#
# Helper: points of an n-pointed star (outer radius r, pointing +Y)
#
def star_points(r, ratio=star_inner_ratio, n=5, rot=math.pi / 2.0):
    pts = []
    for i in range(2 * n):
        ang = rot + i * math.pi / n
        rad = r if i % 2 == 0 else r * ratio
        pts.append((rad * math.cos(ang), rad * math.sin(ang)))
    return pts


# ---- base block, rounded like the Lego brick ----
solid = (
    cq.Workplane("XY")
    .box(total_length, total_width, height)
    .edges("|Z")
    .fillet(5)
    .faces("<Z")
    .fillet(2.5)
)

# ---- cut the grid of cylindrical pockets from the top ----
pocket_cutters = (
    cq.Workplane("XY", origin=(0, 0, top_z))
    .rarray(pitch, pitch, cols, rows, True)
    .circle(cavity_diam / 2.0)
    .extrude(-depth)
)
solid = solid.cut(pocket_cutters)

# ---- raised outlined star on every pocket floor ----
# one star "ring" = outer star with a smaller star removed from its middle
star_ring = (
    cq.Workplane("XY", origin=(0, 0, floor_z))
    .polyline(star_points(star_r)).close()
    .polyline(star_points(star_r * star_outline_scale)).close()
    .extrude(star_h)
)
# stamp it at every cavity centre of the grid, then fuse
xs = [(i - (cols - 1) / 2.0) * pitch for i in range(cols)]
ys = [(j - (rows - 1) / 2.0) * pitch for j in range(rows)]
for x in xs:
    for y in ys:
        solid = solid.union(star_ring.translate((x, y, 0)))

baseplate = (
    cq.Workplane("XY", origin=(0, 0, floor_z))
    .rect(total_length + 15, total_width + 15)
    .rect(total_length - 2 * rim_w, total_width - 2 * rim_w)
    .extrude(-2.5)
)

solid = solid.union(baseplate)

show_object(solid)