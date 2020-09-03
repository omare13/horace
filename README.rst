======
Horace
======

.. start-badges

.. image:: https://img.shields.io/pypi/v/horace.svg
        :target: https://pypi.python.org/pypi/horace

.. image:: https://img.shields.io/travis/linhd-postdata/horace.svg
        :target: https://travis-ci.com/linhd-postdata/horace

.. image:: https://readthedocs.org/projects/horace/badge/?version=latest
        :target: https://horace.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/linhd-postdata/horace/shield.svg
     :target: https://pyup.io/repos/github/linhd-postdata/horace/
     :alt: Updates

.. end-badges

Format converter from PoetryLab JSON to POSTDATA semantic formats


* Free software: Apache Software License 2.0
* Documentation: https://horace.readthedocs.io.


Features
--------

* ``get_scansion_graph()`` receives a scansion dictionary from Rantanplan and outputs an RDFLib Graph object. With it, serialization options become available.

.. code-block:: python

    from rantanplan import get_scansion
    from horace import get_scansion_graph

    poem = """Me gustas cuando callas porque estás como ausente,
    y me oyes desde lejos, y mi voz no te toca.
    Parece que los ojos se te hubieran volado
    y parece que un beso te cerrara la boca.

    Como todas las cosas están llenas de mi alma
    emerges de las cosas, llena del alma mía.
    Mariposa de sueño, te pareces a mi alma,
    y te pareces a la palabra melancolía."""

    scansion = get_scansion(poem)
    graph = get_scansion_graph(scansion)
    graph.serialize(format="xml")

Graphs can be joined together, which is useful when combining graphs generated from scansion, enjambment analysus, or extraction of named entities.


.. code-block:: python

    graphs = []
    graphs.append(get_scansion_graph(scansion1))
    graphs.append(get_scansion_graph(scansion2))

    graph = reduce(lambda x, y: x + y, graphs)  # union on graphs
    graph.serialize(format="xml")

By default, ``xml`` is used to serialize to RDF/XML. Other formats are supported as well, such as ``json-ld``, ``n3``, ``turtle``, and ``nt``.



Credits
-------

*This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.*

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
