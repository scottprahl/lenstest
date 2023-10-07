lenstest
========

by Scott Prahl

.. image:: https://img.shields.io/pypi/v/lenstest?color=68CA66
   :target: https://pypi.org/project/lenstest/
   :alt: pypi

.. image:: https://img.shields.io/github/v/tag/scottprahl/lenstest?label=github&color=v
   :target: https://github.com/scottprahl/lenstest
   :alt: github

.. image:: https://img.shields.io/conda/vn/conda-forge/lenstest?label=conda&color=68CA66
   :target: https://github.com/conda-forge/lenstest-feedstock
   :alt: conda

.. image:: https://zenodo.org/badge/107437651.svg
   :target: https://zenodo.org/badge/latestdoi/107437651
   :alt: zenodo

|

.. image:: https://img.shields.io/github/license/scottprahl/lenstest?color=68CA66
   :target: https://github.com/scottprahl/lenstest/blob/master/LICENSE.txt
   :alt: License

.. image:: https://github.com/scottprahl/lenstest/actions/workflows/test.yaml/badge.svg
   :target: https://github.com/scottprahl/lenstest/actions/workflows/test.yaml
   :alt: testing

.. image:: https://readthedocs.org/projects/lenstest/badge?color=68CA66
  :target: https://lenstest.readthedocs.io
  :alt: docs

.. image:: https://img.shields.io/pypi/dm/lenstest?color=68CA66
   :target: https://pypi.org/project/lenstest/
   :alt: Downloads

__________

`lenstest` is a collection of routines for non-interferometric testing of lenses
and mirrors. Developed by Scott Prahl, this package contains code for the
Foucault Knife Edge Test and the Ronchi Ruling Test. With `lenstest`, users can
test the quality of their lenses and mirrors without the need for
interferometric equipment. 

Detailed documentation is available at
<https://lenstest.readthedocs.io>.


Installation
------------

* Install with ``pip``::
    
    pip install lenstest

or ``conda``::

    conda install -c conda-forge lenstest

or use immediately by clicking the Google Colaboratory button below

.. image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/scottprahl/lenstest/blob/master
   :alt: Colab

Foucault Example
----------------

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import lenstest

    D = 200
    RoC = 400
    z_offset = 10
    x_offset = -0.5
    conic = 0
    phi = np.radians(0)

    foucault.plot_lens_layout(D, RoC, x_offset, z_offset)
    plt.show()

    foucault.plot_knife_and_screen(D, RoC, x_offset, z_offset, phi=phi)
    plt.show()

Produces

.. image:: https://raw.githubusercontent.com/scottprahl/lenstest/master/docs/foucault.png
   :alt: foucougram

Ronchi Example
--------------

10 meter parabolic mirror comparison.

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    import lenstest

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
        x,y = lenstest.ronchi.gram(D, RoC, lp_per_mm, z_offset, conic=conic)
        plt.plot(x,y,'o', markersize=0.1, color='blue')
        lenstest.lenstest.draw_circle(D/2)
        plt.title("%.0fmm from focus"%z_offset)
        plt.gca().set_aspect("equal")
        if i in [1,2,4,5]:
            plt.yticks([])
        if i in [0,1,2]:
            plt.xticks([])
    plt.show()

Produces

.. image:: https://raw.githubusercontent.com/scottprahl/lenstest/master/docs/ronchi.png
   :alt: Ronchigram

License
-------

`lenstest` is licensed under the terms of the MIT license.