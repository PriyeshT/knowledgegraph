"""
RAG Application with Knowledge Graph
----------------------------------
This example demonstrates how to use a knowledge graph for RAG (Retrieval Augmented Generation)
to answer questions about the data.
"""

import networkx as nx
from typing import Dict, List, Any, Tuple, Optional
import spacy
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class KnowledgeGraphRAG:
    def __init__(self):
        """Initialize the RAG system with knowledge graph."""
        self.graph = nx.Graph()
        # Load English language model for NLP
        self.nlp = spacy.load("en_core_web_sm")
        # Load sentence transformer for semantic search
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
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
        
        # Create embeddings for nodes and relationships
        self._create_embeddings()
    
    def _extract_entities(self, doc) -> List[Tuple[str, str, Dict[str, str]]]:
        """Extract entities from the text."""
        entities = []
        for ent in doc.ents:
            entity_id = f"{ent.label_}_{ent.text.lower().replace(' ', '_')}"
            properties = {
                'text': ent.text,
                'type': ent.label_,
                'start_char': ent.start_char,
                'end_char': ent.end_char
            }
            entities.append((entity_id, ent.label_, properties))
        return entities
    
    def _extract_relationships(self, doc) -> List[Tuple[str, str, str, str, str, str]]:
        """Extract relationships between entities using dependency parsing."""
        relationships = []
        for token in doc:
            if token.dep_ in ('nsubj', 'nsubjpass'):
                subject = token
                verb = token.head
                for child in verb.children:
                    if child.dep_ in ('dobj', 'pobj'):
                        subject_type = subject.ent_type_ if subject.ent_type_ else 'UNKNOWN'
                        object_type = child.ent_type_ if child.ent_type_ else 'UNKNOWN'
                        subject_id = f"{subject_type}_{subject.text.lower().replace(' ', '_')}"
                        object_id = f"{object_type}_{child.text.lower().replace(' ', '_')}"
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
            self.graph.add_node(
                entity_id,
                type=entity_type,
                text=properties['text'],
                color=self._get_entity_color(entity_type)
            )
    
    def _add_relationships_to_graph(self, relationships: List[Tuple[str, str, str, str, str, str]]) -> None:
        """Add relationships as edges to the graph."""
        for subject_id, subject_type, relation, object_id, object_type, context in relationships:
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
            self.graph.add_edge(
                subject_id,
                object_id,
                relationship=relation,
                context=context,
                color='blue'
            )
    
    def _create_embeddings(self) -> None:
        """Create embeddings for nodes and relationships for semantic search."""
        # Create embeddings for nodes
        for node in self.graph.nodes():
            node_text = self.graph.nodes[node]['text']
            self.graph.nodes[node]['embedding'] = self.encoder.encode(node_text)
        
        # Create embeddings for relationships
        for edge in self.graph.edges():
            edge_context = self.graph.edges[edge]['context']
            self.graph.edges[edge]['embedding'] = self.encoder.encode(edge_context)
    
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
    
    def _find_relevant_nodes(self, query: str, top_k: int = 3) -> List[str]:
        """Find nodes most relevant to the query using semantic search."""
        query_embedding = self.encoder.encode(query)
        node_scores = []
        
        for node in self.graph.nodes():
            node_embedding = self.graph.nodes[node]['embedding']
            similarity = cosine_similarity([query_embedding], [node_embedding])[0][0]
            node_scores.append((node, similarity))
        
        # Sort by similarity score and return top k nodes
        node_scores.sort(key=lambda x: x[1], reverse=True)
        return [node for node, _ in node_scores[:top_k]]
    
    def _find_relevant_relationships(self, query: str, top_k: int = 3) -> List[Tuple[str, str, str]]:
        """Find relationships most relevant to the query using semantic search."""
        query_embedding = self.encoder.encode(query)
        relationship_scores = []
        
        for edge in self.graph.edges():
            edge_embedding = self.graph.edges[edge]['embedding']
            similarity = cosine_similarity([query_embedding], [edge_embedding])[0][0]
            relationship_scores.append((edge, similarity))
        
        # Sort by similarity score and return top k relationships
        relationship_scores.sort(key=lambda x: x[1], reverse=True)
        return [(edge[0], edge[1], self.graph.edges[edge]['context']) 
                for edge, _ in relationship_scores[:top_k]]
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question using the knowledge graph.
        
        Parameters:
        - question: The question to answer
        
        Returns:
        - A natural language answer
        """
        # Find relevant nodes and relationships
        relevant_nodes = self._find_relevant_nodes(question)
        relevant_relationships = self._find_relevant_relationships(question)
        
        # Build context from relevant information
        context = []
        
        # Add information about relevant nodes
        for node in relevant_nodes:
            node_text = self.graph.nodes[node]['text']
            node_type = self.graph.nodes[node]['type']
            context.append(f"{node_text} is a {node_type}")
        
        # Add information about relevant relationships
        for subject, object, relation in relevant_relationships:
            subject_text = self.graph.nodes[subject]['text']
            object_text = self.graph.nodes[object]['text']
            context.append(f"{subject_text} {relation} {object_text}")
        
        # Generate a natural language answer
        if not context:
            return "I don't have enough information to answer that question."
        
        # Combine context into a coherent answer
        answer = "Based on the available information: "
        answer += ". ".join(context)
        answer += "."
        
        return answer

def demonstrate_rag_system():
    """Demonstrate the RAG system with knowledge graph."""
    # Sample text about a company
    text = """
    Apple Inc. is a technology company headquartered in Cupertino, California.
    Steve Jobs and Steve Wozniak founded Apple in 1976.
    The company launched the iPhone in 2007, which revolutionized the smartphone industry.
    Tim Cook became CEO in 2011 after Steve Jobs stepped down.
    Apple's market value reached $3 trillion in 2022.
    The company is known for its innovative products like the Mac, iPad, and Apple Watch.
    """
    
    # Create and initialize the RAG system
    rag = KnowledgeGraphRAG()
    rag.build_from_text(text)
    
    # Example questions
    questions = [
        "Who founded Apple?",
        "When was the iPhone launched?",
        "What is Apple's market value?",
        "Who is the current CEO of Apple?",
        "What products does Apple make?"
    ]
    
    # Answer questions
    print("Knowledge Graph RAG System Demo")
    print("================================")
    for question in questions:
        print(f"\nQuestion: {question}")
        answer = rag.answer_question(question)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    demonstrate_rag_system() 