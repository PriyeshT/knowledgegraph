"""
Building Knowledge Graphs from Data
---------------------------------
This example demonstrates how to build a knowledge graph from structured data,
showing how to identify nodes, edges, properties, and types from real data.
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Any
import json

class DataDrivenKnowledgeGraph:
    def __init__(self):
        """Initialize an empty knowledge graph."""
        self.graph = nx.Graph()
        
    def build_from_json(self, data: Dict[str, Any]) -> None:
        """
        Build a knowledge graph from JSON data.
        
        Parameters:
        - data: Dictionary containing the structured data
        """
        # First, identify and add all nodes
        self._add_nodes_from_data(data)
        
        # Then, identify and add all relationships
        self._add_relationships_from_data(data)
    
    def _add_nodes_from_data(self, data: Dict[str, Any]) -> None:
        """Add nodes to the graph based on the data structure."""
        # Add company node
        company_id = f"company_{data['company']['id']}"
        self.graph.add_node(
            company_id,
            type='company',
            name=data['company']['name'],
            industry=data['company']['industry'],
            color='lightblue'
        )
        
        # Add departments
        for dept in data['departments']:
            dept_id = f"dept_{dept['id']}"
            self.graph.add_node(
                dept_id,
                type='department',
                name=dept['name'],
                location=dept['location'],
                color='lightgreen'
            )
        
        # Add employees
        for emp in data['employees']:
            emp_id = f"emp_{emp['id']}"
            self.graph.add_node(
                emp_id,
                type='employee',
                name=emp['name'],
                role=emp['role'],
                color='lightpink'
            )
        
        # Add projects
        for proj in data['projects']:
            proj_id = f"proj_{proj['id']}"
            self.graph.add_node(
                proj_id,
                type='project',
                name=proj['name'],
                status=proj['status'],
                color='lightyellow'
            )
    
    def _add_relationships_from_data(self, data: Dict[str, Any]) -> None:
        """Add relationships to the graph based on the data structure."""
        # Link departments to company
        for dept in data['departments']:
            dept_id = f"dept_{dept['id']}"
            company_id = f"company_{data['company']['id']}"
            self.graph.add_edge(
                dept_id,
                company_id,
                relationship_type='belongs_to',
                color='blue'
            )
        
        # Link employees to departments
        for emp in data['employees']:
            emp_id = f"emp_{emp['id']}"
            dept_id = f"dept_{emp['department_id']}"
            self.graph.add_edge(
                emp_id,
                dept_id,
                relationship_type='works_in',
                color='green'
            )
        
        # Link employees to projects
        for proj in data['projects']:
            proj_id = f"proj_{proj['id']}"
            for emp_id in proj['employee_ids']:
                emp_node_id = f"emp_{emp_id}"
                self.graph.add_edge(
                    emp_node_id,
                    proj_id,
                    relationship_type='works_on',
                    color='red'
                )
    
    def visualize_graph(self, title: str = "Company Knowledge Graph") -> None:
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
            labels={node: self.graph.nodes[node]['name'] for node in self.graph.nodes()}
        )
        
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

def demonstrate_data_driven_graph():
    """Demonstrate building a knowledge graph from structured data."""
    # Sample company data
    company_data = {
        "company": {
            "id": 1,
            "name": "TechCorp",
            "industry": "Technology"
        },
        "departments": [
            {
                "id": 1,
                "name": "Engineering",
                "location": "San Francisco"
            },
            {
                "id": 2,
                "name": "Marketing",
                "location": "New York"
            }
        ],
        "employees": [
            {
                "id": 1,
                "name": "Alice Smith",
                "role": "Software Engineer",
                "department_id": 1
            },
            {
                "id": 2,
                "name": "Bob Johnson",
                "role": "Marketing Manager",
                "department_id": 2
            },
            {
                "id": 3,
                "name": "Carol White",
                "role": "Product Manager",
                "department_id": 1
            }
        ],
        "projects": [
            {
                "id": 1,
                "name": "Website Redesign",
                "status": "In Progress",
                "employee_ids": [1, 3]
            },
            {
                "id": 2,
                "name": "Brand Campaign",
                "status": "Planning",
                "employee_ids": [2]
            }
        ]
    }
    
    # Create and build the graph
    graph = DataDrivenKnowledgeGraph()
    graph.build_from_json(company_data)
    
    # Visualize the graph
    graph.visualize_graph()

if __name__ == "__main__":
    demonstrate_data_driven_graph() 