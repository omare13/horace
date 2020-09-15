"""Core module."""

from owlready2 import Ontology, get_ontology
from rdflib import Graph
from slugify import slugify

from horace.utils import ONTOLOGIES, RESOURCES_IRI, onto_to_graph


def get_averell_core_graph(source: str, poem: dict) -> Graph:
    """Transform an Averell poem dictionary into a compliant LOD graph.
    :param source: str with corpus source name
    :param poem: Dictionary with a Averell-like poem data
    :return: RDFLib Graph with the individuals from poem
    """
    core_onto = get_ontology(ONTOLOGIES["core"]).load()
    onto = add_core_individuals(source, poem, core_onto)
    classes = [onto.PoeticWork, onto.Redaction, onto.CreatorRole]
    return onto_to_graph(onto, classes)


def filter_individuals(graph: Graph, s: int, *args) -> bool:
    """Filtering function to keep just the individuals of the classes
    we are interested in when serializing.
    :param graph: OWLReady2 graph
    :param s: storeid specifying an individual in graph.onto
    :return: Boolean deciding whether the instance specified by its storeid
             should be returned or not
    """
    classes = [graph.onto.PoeticWork, graph.onto.Redaction,
               graph.onto.CreatorRole]
    return s >= 0 and any(isinstance(graph.onto.world._get_by_storid(s), cls)
                          for cls in classes)


def add_core_individuals(source: str, poem: dict, onto: Ontology) -> Ontology:
    """Transform an Averell poem dictionary into an OWLReady ontology.
    This function performs all changes directly on onto.
    :param source: str with corpus source name
    :param poem: Dictionary with an Averell-like poem data
    :param onto: OWLReady2 ontology
    :return: The modified ontology onto
    """
    poem_title = poem["poem_title"]
    author = poem["author"]
    slug_title = slugify(poem_title, separator='_')
    slug_author = slugify(author)
    o_poetic_work = onto.PoeticWork(iri=f"{RESOURCES_IRI}PW_{slug_title}")
    o_redaction = onto.Redaction(iri=f"{RESOURCES_IRI}R_{slug_title}_{source}")
    o_creator_role = onto.CreatorRole(iri=f"{RESOURCES_IRI}CR_{slug_author}")
    o_poetic_work.isRealisedThrough = [o_redaction]
    o_redaction.hasCreator = [o_creator_role]
    return onto
