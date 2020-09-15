"""Structural module"""
import uuid
from typing import List

from owlready2 import Ontology, get_ontology
from rdflib import Graph

from horace.utils import ONTOLOGIES, RESOURCES_IRI, onto_to_graph


def get_scansion_graph(scansion: dict) -> Graph:
    """Transform a scansion dictionary into a compliant LOD graph.
    :param scansion: Dictionary with a Rantanplan-like scansion analysis
    :return: RDFLib Graph with the individuals from scansion
    """
    structural_onto = get_ontology(ONTOLOGIES["structural"]).load()
    onto = add_structural_individuals(scansion, structural_onto)
    classes = [onto.Stanza, onto.Line, onto.Word, onto.Syllable]
    return onto_to_graph(onto, classes)


def filter_individuals(graph: Graph, s: int, *args) -> bool:
    """Filtering function to keep just the individuals of the classes
    we are interested in when serializing.
    :param graph: OWLReady2 graph
    :param s: storeid specifying an individual in graph.onto
    :return: Boolean deciding whether the instance specified by its storeid
             should be returned or not
    """
    classes = [graph.onto.Stanza, graph.onto.Line, graph.onto.Word,
               graph.onto.Syllable]
    return s >= 0 and any(isinstance(graph.onto.world._get_by_storid(s), cls)
                          for cls in classes)


def add_structural_individuals(scansion: dict, onto: Ontology) -> Ontology:
    """Transform a Rantanplan scansion dictionary into an OWLReady ontology.
    This function performs all changes directly on onto.
    :param scansion: Dictionary with a Rantanplan-like scansion analysis
    :param onto: OWLReady2 ontology
    :return: The modified ontology onto
    """
    for line in scansion:
        if "tokens" not in line:
            continue
        o_line = onto.Line(
            f"{onto.Line.name}/{uuid.uuid4()}",
            content=[join_tokens(line["tokens"])],
        )
        o_line.iri = f"{RESOURCES_IRI}L_{uuid.uuid4()}"
        o_line.has_words = []
        for token in line["tokens"]:
            o_word = onto.Word(
                f"{onto.Word.name}/{uuid.uuid4()}",
                content=[join_syllables(token)],
                belongsToLine=[o_line],
            )
            o_word.has_syllables = []
            if "word" not in token:
                continue
            for syllable in token["word"]:
                o_syllable = onto.Syllable(
                    f"{onto.Syllable.name}/{uuid.uuid4()}",
                    content=[syllable["syllable"]],
                    belongsToWord=[o_word],
                )
                o_word.has_syllables += [o_syllable]
            o_line.has_words += [o_word]
    return onto


def join_tokens(tokens: List[str]) -> str:
    """Join all words from a list of tokens into a string.
    :param tokens: List of dictionaries representing tokens
    :return: String of words
    """
    output = []
    for token in tokens:
        item = join_syllables(token)
        output.append(item)
    return " ".join(output)


def join_syllables(token: List[dict]) -> str:
    """Join all symbols and syllables from a list of tokens into a string."
    :param token: List of dictionaries representing tokens
    :return: String of syllables
    """
    if "symbol" in token:
        return token["symbol"]
    else:
        return "".join([syll["syllable"] for syll in token["word"]])


def get_averell_structural_graph(poem: dict) -> Graph:
    """Transform a scansion dictionary into a compliant LOD graph.
    :param poem: Dictionary with a Rantanplan-like scansion analysis
    :return: RDFLib Graph with the individuals from scansion
    """
    structural_onto = get_ontology(ONTOLOGIES["structural"]).load()
    onto = add_averell_structural_individuals(poem, structural_onto)
    classes = [onto.Stanza, onto.Line, onto.Word, onto.Syllable]
    return onto_to_graph(onto, classes)


def add_averell_structural_individuals(poem: dict, onto: Ontology) -> Ontology:
    """Transform an Averell scansion dictionary into an OWLReady ontology.
    This function performs all changes directly on onto.
    :param poem: Dictionary with an Averell-like poem data
    :param onto: OWLReady2 ontology
    :return: The modified ontology onto
    """
    for stanza in poem["stanzas"]:
        o_stanza = onto.Stanza(iri=f"{RESOURCES_IRI}ST_{uuid.uuid4()}",
                               content=[stanza["stanza_text"]])
        for line in stanza["lines"]:
            o_line = onto.Line(iri=f"{RESOURCES_IRI}L_{uuid.uuid4()}",
                               content=[line["line_text"]])
            o_line.has_words = []
            if "words" not in line:
                continue
            for word in line["words"]:
                o_word = onto.Word(iri=f"{RESOURCES_IRI}W_{uuid.uuid4()}",
                                   content=[word["word_text"]],
                                   belongsToLine=[o_line])
                o_word.has_syllables = []
                if "syllables" not in word:
                    continue
                for syllable in word["syllables"]:
                    o_syllable = onto.Syllable(
                        iri=f"{RESOURCES_IRI}SY_{uuid.uuid4()}",
                        content=[syllable],
                        belongsToWord=[o_word])
                    o_word.has_syllables += [o_syllable]
                o_line.has_words += [o_word]
            o_stanza.hasLine += [o_line]
    return onto
