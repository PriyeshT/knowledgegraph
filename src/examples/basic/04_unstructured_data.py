"""
Building Knowledge Graphs from Unstructured Data
---------------------------------------------
This example demonstrates how to build a knowledge graph from unstructured text data
using Natural Language Processing (NLP) techniques.
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple
import spacy
from collections import defaultdict

class UnstructuredDataGraph:
    def __init__(self):
        """Initialize an empty knowledge graph."""
        self.graph = nx.Graph()
        # Load English language model
        self.nlp = spacy.load("en_core_web_sm")
        
    def build_from_text(self, text: str) -> None:
        """
        Build a knowledge graph from unstructured text.
        
        Parameters:
        - text: The input text to analyze
        """
        # Process the text with spaCy
        doc = self.nlp(text)
        
        # Extract entities and relationships
        entities = self._extract_entities(doc)
        relationships = self._extract_relationships(doc)
        
        # Add nodes and edges to the graph
        self._add_entities_to_graph(entities)
        self._add_relationships_to_graph(relationships)
    
    def _extract_entities(self, doc) -> List[Tuple[str, str, Dict[str, str]]]:
        """
        Extract entities from the text.
        
        Returns:
        - List of tuples containing (entity_id, entity_type, properties)
        """
        entities = []
        for ent in doc.ents:
            # Create a unique ID for the entity
            entity_id = f"{ent.label_}_{ent.text.lower().replace(' ', '_')}"
            
            # Create properties for the entity
            properties = {
                'text': ent.text,
                'type': ent.label_,
                'start_char': ent.start_char,
                'end_char': ent.end_char
            }
            
            entities.append((entity_id, ent.label_, properties))
        
        return entities
    
    def _extract_relationships(self, doc) -> List[Tuple[str, str, str, str, str, str]]:
        """
        Extract relationships between entities using dependency parsing.
        
        Returns:
        - List of tuples containing (subject_id, subject_type, relationship, object_id, object_type, context)
        """
        relationships = []
        
        for token in doc:
            # Look for subject-verb-object patterns
            if token.dep_ in ('nsubj', 'nsubjpass'):
                subject = token
                verb = token.head
                
                # Find the object
                for child in verb.children:
                    if child.dep_ in ('dobj', 'pobj'):
                        # Get entity types
                        subject_type = subject.ent_type_ if subject.ent_type_ else 'UNKNOWN'
                        object_type = child.ent_type_ if child.ent_type_ else 'UNKNOWN'
                        
                        # Create entity IDs
                        subject_id = f"{subject_type}_{subject.text.lower().replace(' ', '_')}"
                        object_id = f"{object_type}_{child.text.lower().replace(' ', '_')}"
                        
                        # Add the relationship
                        relationships.append((
                            subject_id,
                            subject_type,
                            verb.lemma_,
                            object_id,
                            object_type,
                            f"{subject.text} {verb.text} {child.text}"
                        ))
        
        return relationships
    
    def _add_entities_to_graph(self, entities: List[Tuple[str, str, Dict[str, str]]]) -> None:
        """Add entities as nodes to the graph."""
        for entity_id, entity_type, properties in entities:
            # Add color based on entity type
            color = self._get_entity_color(entity_type)
            
            # Add the node with its properties
            self.graph.add_node(
                entity_id,
                type=entity_type,
                text=properties['text'],
                color=color
            )
    
    def _add_relationships_to_graph(self, relationships: List[Tuple[str, str, str, str, str, str]]) -> None:
        """Add relationships as edges to the graph."""
        for subject_id, subject_type, relation, object_id, object_type, context in relationships:
            # Add nodes if they don't exist
            if subject_id not in self.graph:
                self.graph.add_node(
                    subject_id,
                    type=subject_type,
                    text=subject_id.split('_', 1)[1].replace('_', ' ').title(),
                    color=self._get_entity_color(subject_type)
                )
            
            if object_id not in self.graph:
                self.graph.add_node(
                    object_id,
                    type=object_type,
                    text=object_id.split('_', 1)[1].replace('_', ' ').title(),
                    color=self._get_entity_color(object_type)
                )
            
            # Add the edge with the relationship information
            self.graph.add_edge(
                subject_id,
                object_id,
                relationship=relation,
                context=context,
                color='blue'
            )
    
    def _get_entity_color(self, entity_type: str) -> str:
        """Get a color for visualization based on entity type."""
        colors = {
            'ORG': 'lightblue',
            'PERSON': 'lightpink',
            'GPE': 'lightgreen',
            'DATE': 'lightyellow',
            'MONEY': 'lightgray',
            'PRODUCT': 'lightcoral',
            'EVENT': 'lightseagreen',
            'UNKNOWN': 'white'
        }
        return colors.get(entity_type, 'white')
    
    def visualize_graph(self, title: str = "Knowledge Graph from Text") -> None:
        """Visualize the knowledge graph."""
        plt.figure(figsize=(15, 10))
        
        # Get node colors
        node_colors = [self.graph.nodes[node]['color'] for node in self.graph.nodes()]
        
        # Get edge colors
        edge_colors = [self.graph.edges[edge]['color'] for edge in self.graph.edges()]
        
        # Create the layout
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        
        # Draw the graph
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=2000,
            font_size=8,
            font_weight='bold',
            labels={node: self.graph.nodes[node]['text'] for node in self.graph.nodes()}
        )
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def demonstrate_unstructured_graph():
    """Demonstrate building a knowledge graph from unstructured text."""
    # Sample text about a company
    text = """
    Apple Inc. is a technology company headquartered in Cupertino, California.
    Steve Jobs and Steve Wozniak founded Apple in 1976.
    The company launched the iPhone in 2007, which revolutionized the smartphone industry.
    Tim Cook became CEO in 2011 after Steve Jobs stepped down.
    Apple's market value reached $3 trillion in 2022.
    The company is known for its innovative products like the Mac, iPad, and Apple Watch.
    """
    
    # Create and build the graph
    graph = UnstructuredDataGraph()
    graph.build_from_text(text)
    
    # Visualize the graph
    graph.visualize_graph()

if __name__ == "__main__":
    demonstrate_unstructured_graph() 