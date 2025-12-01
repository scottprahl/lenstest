.. |pypi| image:: https://img.shields.io/pypi/v/lenstest?color=68CA66
   :target: https://pypi.org/project/lenstest/
   :alt: pypi

.. |github| image:: https://img.shields.io/github/v/tag/scottprahl/lenstest?label=github&color=v
   :target: https://github.com/scottprahl/lenstest
   :alt: github

.. |conda| image:: https://img.shields.io/conda/vn/conda-forge/lenstest?label=conda&color=68CA66
   :target: https://github.com/conda-forge/lenstest-feedstock
   :alt: conda

.. |doi| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.8417590.svg
   :target: https://doi.org/10.5281/zenodo.8417590
   :alt: DOI

.. |license| image:: https://img.shields.io/github/license/scottprahl/lenstest?color=68CA66
   :target: https://github.com/scottprahl/lenstest/blob/main/LICENSE.txt
   :alt: License

.. |test| image:: https://github.com/scottprahl/lenstest/actions/workflows/test.yaml/badge.svg
   :target: https://github.com/scottprahl/lenstest/actions/workflows/test.yaml
   :alt: testing

.. |docs| image:: https://readthedocs.org/projects/lenstest/badge?color=68CA66
  :target: https://lenstest.readthedocs.io
  :alt: docs

.. |downloads| image:: https://img.shields.io/pypi/dm/lenstest?color=68CA66
   :target: https://pypi.org/project/lenstest/
   :alt: Downloads

.. |lite| image:: https://img.shields.io/badge/try-JupyterLite-68CA66.svg
   :target: https://scottprahl.github.io/lenstest/
   :alt: Try JupyterLite


lenstest
========

by Scott Prahl

|pypi| |github| |conda| |doi|

|license| |test| |docs| |downloads|

|lite|

__________

``lenstest`` is a collection of routines for non-interferometric testing of lenses
and mirrors. Developed by Scott Prahl, this package contains code for the
Foucault Knife Edge Test and the Ronchi Ruling Test. With `lenstest`, users can
test the quality of their lenses and mirrors without the need for
interferometric equipment. 

Detailed documentation is available at <https://lenstest.readthedocs.io>.


Installation
------------

* Install with ``pip``::
    
    pip install lenstest

* or with ``conda``::

    conda install -c conda-forge lenstest

or use immediately by clicking the Jupyterlite button below

    |lite|

Foucault Example
----------------

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from lenstest import foucault

    D = 200
    RoC = 400
    z_offset = 10
    x_offset = -0.5
    phi = np.radians(0)

    foucault.plot_lens_layout(D, RoC, x_offset, z_offset)
    plt.show()

    foucault.plot_knife_and_screen(D, RoC, x_offset, z_offset, phi=phi)
    plt.show()

Produces

.. image:: https://raw.githubusercontent.com/scottprahl/lenstest/main/docs/foucault_layout.png
   :alt: layout

.. image:: https://raw.githubusercontent.com/scottprahl/lenstest/main/docs/foucault_diagram.png
   :alt: foucougram

Ronchi Example
--------------

10 meter parabolic mirror comparison.

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from lenstest import ronchi
    from lenstest.lenstest import draw_circle

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
        lenstest.draw_circle(D/2)
        plt.title("%.0fmm from focus"%z_offset)
        plt.gca().set_aspect("equal")
        if i in [1,2,4,5]:
            plt.yticks([])
        if i in [0,1,2]:
            plt.xticks([])
    plt.show()

Produces

.. code-block: text

        Mirror Diameter = 10000 mm
                     F# = 5.0
    Radius of Curvature = 100000 mm
           Focal Length = 50000 mm
       Ronchi Frequency = 0.133 lp/mm

.. image:: https://raw.githubusercontent.com/scottprahl/lenstest/main/docs/ronchi.png
   :alt: Ronchigram

Citation
--------

If you use lenstest in academic, instructional, or applied technical work, please cite:

Prahl, S. (2023). lenstest: A Python module for non-interferometric testing of mirrors and lenses (Version 1.0.0) 
Computer Software. Zenodo. https://doi.org/10.5281/zenodo.8417590

BibTeX
^^^^^^

.. code-block:: bibtex

    @software{lenstest_prahl_2023,
    author = {Scott Prahl},
    title = {lenstest: A Python module for non-interferometric testing of mirrors and lenses},
    year = {2023},
    version = {1.0.0},
    doi = {10.5281/zenodo.8417590},
    url = {https://github.com/scottprahl/lenstest},
    publisher = {Zenodo}
    }

License
-------

``lenstest`` is licensed under the terms of the MIT license.
