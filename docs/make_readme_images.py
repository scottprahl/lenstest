import numpy as np
import matplotlib.pyplot as plt
from lenstest import foucault, ronchi
from lenstest.lenstest import draw_circle

def make_foucault_images():
    """Create first two images."""
    D = 200
    RoC = 400
    z_offset = 10
    x_offset = -0.5
    conic = 0
    phi = np.radians(0)

    foucault.plot_lens_layout(D, RoC, x_offset, z_offset)
    plt.savefig("foucault_layout.png", dpi=300)
#    plt.show()

    foucault.plot_knife_and_screen(D, RoC, x_offset, z_offset, phi=phi)
    plt.savefig("foucault_diagram.png", dpi=300)
#    plt.show()

def make_ronchi_images():

    D = 10000  # 10 meter mirror
    F = 5
    conic = -1
    lp_per_mm = 0.133  # grating frequency lp/mm

    RoC =  F * D * 2

    print("    Mirror Diameter = %.0f mm" % D)
    print("                 F# = %.1f" % F)
    print("Radius of Curvature = %.0f mm" % RoC)
    print("       Focal Length = %.0f mm" % (RoC/2))
    print("   Ronchi Frequency = %.3f lp/mm" % lp_per_mm)

    plt.subplots(2,3,figsize=(13,8))

    for i, z_offset in enumerate([-63,35,133,231,329,429]):
        plt.subplot(2,3,i+1)
        x,y = ronchi.gram(D, RoC, lp_per_mm, z_offset, conic=conic)
        plt.plot(x,y,'o', markersize=0.1, color='blue')
        draw_circle(D/2)
        plt.title("%.0fmm from focus"%z_offset)
        plt.gca().set_aspect("equal")
        if i in [1,2,4,5]:
            plt.yticks([])
        if i in [0,1,2]:
            plt.xticks([])
    plt.savefig("ronchi.png", dpi=300)
#    plt.show()

def main():
    make_foucault_images()
    make_ronchi_images()
 
# Run the test case
if __name__ == "__main__":
    main()
