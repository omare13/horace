"""Utils module"""
import io
from functools import partial
from typing import List, Optional

from owlready2 import Ontology
from rdflib import Graph

ONTOLOGY_URL_TEMPLATE = ("https://raw.githubusercontent.com/linhd-postdata/"
                         "{onto}-ontology/master/postdata-{onto}.owl")
ONTOLOGIES = {
    "core": ONTOLOGY_URL_TEMPLATE.format(onto="core"),
    "structural": ONTOLOGY_URL_TEMPLATE.format(onto="structuralElements"),
    "prosodic": ONTOLOGY_URL_TEMPLATE.format(onto="prosodicElements"),
    "literary": ONTOLOGY_URL_TEMPLATE.format(onto="literaryAnalysis"),
}

RESOURCES_IRI = "http://postdata.linhd.uned.es/resource/"


def onto_to_graph(onto: Ontology, classes: Optional[List] = None) -> Graph:
    """Convert an OWLReady2 ontology graph to RDFLib.
    :param onto: OWLReady2 ontology
    :param classes: List of ontology classes to filter individuals
    :return: RDFLib Graph
    """
    with io.BytesIO() as file:
        onto.save(
            file=file,
            format="rdfxml",
            filter=partial(filter_individuals, classes=classes)
        )
        rdf = file.getvalue().decode("utf8")
        return Graph().parse(data=rdf)


def filter_individuals(graph: Graph, s: int, *args,
                       classes: Optional[List] = None) -> bool:
    """Filtering function to keep just the individuals of the classes
    we are interested in when serializing.
    :param graph: OWLReady2 graph
    :param s: storeid specifying an individual in graph.onto
    :param classes: List of ontology classes to filter individuals
    :return: Boolean deciding whether the instance specified by its storeid
             should be returned or not
    """
    if not classes:
        classes = [graph.onto.Line, graph.onto.Word, graph.onto.Syllable]
    return s >= 0 and any(isinstance(graph.onto.world._get_by_storid(s), cls)
                          for cls in classes)
