from equations import *
import matplotlib.pyplot as plt
import solver

gamma = 5 / 3
M_e = 2.4

# Run the MoC solver with its default values.
init_chars, wall_points = solver.solve_min_length_nozzle(M_e, gamma)

# Get coordinates for all wall points.
wall_xs = []
wall_ys = []
for p in wall_points:
    wall_xs.append(p.x)
    wall_ys.append(p.y)

# Get coordinates for all points.
all_p_xs = []
all_p_ys = []
for char in init_chars:
    for p in char.points:
        if all_p_xs.count(p.x) == 0 or all_p_ys.count(p.y) == 0:
            all_p_xs.append(p.x)
            all_p_ys.append(p.y)

# Create a line of symmetry that can also be used to show wall point distribution along the x axis.
flat = []
for x in wall_xs:
    flat.append(0)

fig = plt.figure()
fig.patch.set_facecolor('white')
ax = fig.gca()

ax.plot(wall_xs, wall_ys)  # Nozzle contour plot.
ax.plot(wall_xs, wall_ys, 'gx')  # Wall point distribution plot

# ax.plot(all_p_xs, all_p_ys, 'gx')  # Uncomment to show all points.

# Show the area ratio on the plot.
a_ratio = area_ratio(M_e, gamma)
ax.plot(wall_xs[-1], a_ratio, 'ro')
ax.annotate("$A/A^{*}$", (wall_xs[-1], a_ratio), (wall_xs[-1] - 0.6, a_ratio - 0.2),
            arrowprops={"arrowstyle": "->"})

ax.plot(wall_xs, flat, 'r--')  # Draws the line of symmetry. Change to 'ro' to show wall point distribution.
ax.set_xlabel(r'$x/r_{a}$')  # Label the x axis.
ax.set_ylabel(r'$y/r_{a}$')  # Label the y axis.
ax.axis([0, wall_xs[-1] + 0.1, -0.1, wall_ys[-1] + 0.1])  # Set axis bounds to show full contour.
plt.show()

# Output useful values for analysis.
print("Area ratio at final point = {0:.3f}".format(a_ratio))
print("Final point y coordinate = {0:.3f}".format(wall_ys[-1]))
