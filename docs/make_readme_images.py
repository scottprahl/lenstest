"""Create the images needed for README.rst."""

import matplotlib.pyplot as plt
import lenstest

def make_foucault_images():
    """Create Foucault image for README.rst."""
    D = 200
    RoC = 400
    z_offset = 10
    x_offset = -0.5

    lenstest.foucault.plot_lens_layout(D, RoC, x_offset, z_offset)
    plt.savefig("foucault.png", dpi=300)
    # plt.show()


def make_ronchi_images():
    """Create Ronchi image for README.rst."""
    D = 10000  # 10 meter mirror
    F = 5
    conic = -1
    lp_per_mm = 0.133  # grating frequency lp/mm

    RoC = F * D * 2

    print("    Mirror Diameter = %.0f mm" % D)
    print("                 F# = %.1f" % F)
    print("Radius of Curvature = %.0f mm" % RoC)
    print("       Focal Length = %.0f mm" % (RoC / 2))
    print("   Ronchi Frequency = %.3f lp/mm" % lp_per_mm)

    plt.subplots(2, 3, figsize=(13, 8))

    for i, z_offset in enumerate([-63, 35, 133, 231, 329, 429]):
        plt.subplot(2, 3, i + 1)
        x, y = lenstest.ronchi.gram(D, RoC, lp_per_mm, z_offset, conic=conic)
        plt.plot(x, y, "o", markersize=0.1, color="blue")
        lenstest.lenstest.draw_circle(D / 2)
        plt.title("%.0fmm from focus" % z_offset)
        plt.gca().set_aspect("equal")
        if i in [1, 2, 4, 5]:
            plt.yticks([])
        if i in [0, 1, 2]:
            plt.xticks([])
    plt.savefig("ronchi.png", dpi=300)
    # plt.show()


def main():
    """Create all images for README.rst."""
    make_foucault_images()
    make_ronchi_images()


# Run the test case
if __name__ == "__main__":
    main()
