"""
Product Catalog Knowledge Graph Example
-------------------------------------
This example demonstrates how to create a simple knowledge graph for a product catalog.
We'll use NetworkX, a popular Python library for working with graphs.

Key Concepts Demonstrated:
1. Nodes (Entities): Products, Categories, Features
2. Edges (Relationships): belongs_to, has_feature
3. Properties: price, description, etc.
"""

import networkx as nx
from typing import Dict, List, Any

class ProductCatalogGraph:
    def __init__(self):
        """
        Initialize an empty knowledge graph.
        Think of this as creating a blank canvas where we'll draw our product relationships.
        """
        self.graph = nx.Graph()
        
    def add_product(self, product_id: str, name: str, price: float, description: str) -> None:
        """
        Add a product to the graph.
        
        Parameters:
        - product_id: Unique identifier for the product
        - name: Product name
        - price: Product price
        - description: Product description
        
        This creates a node (entity) in our graph with properties.
        """
        # Add the product as a node with its properties
        self.graph.add_node(
            product_id,
            type='product',
            name=name,
            price=price,
            description=description
        )
    
    def add_category(self, category_id: str, name: str, description: str) -> None:
        """
        Add a product category to the graph.
        
        Parameters:
        - category_id: Unique identifier for the category
        - name: Category name
        - description: Category description
        """
        self.graph.add_node(
            category_id,
            type='category',
            name=name,
            description=description
        )
    
    def add_feature(self, feature_id: str, name: str, description: str) -> None:
        """
        Add a product feature to the graph.
        
        Parameters:
        - feature_id: Unique identifier for the feature
        - name: Feature name
        - description: Feature description
        """
        self.graph.add_node(
            feature_id,
            type='feature',
            name=name,
            description=description
        )
    
    def link_product_to_category(self, product_id: str, category_id: str) -> None:
        """
        Create a relationship between a product and its category.
        
        Parameters:
        - product_id: ID of the product
        - category_id: ID of the category
        
        This creates an edge (relationship) in our graph.
        """
        self.graph.add_edge(
            product_id,
            category_id,
            relationship_type='belongs_to'
        )
    
    def link_product_to_feature(self, product_id: str, feature_id: str) -> None:
        """
        Create a relationship between a product and its features.
        
        Parameters:
        - product_id: ID of the product
        - feature_id: ID of the feature
        """
        self.graph.add_edge(
            product_id,
            feature_id,
            relationship_type='has_feature'
        )
    
    def get_product_info(self, product_id: str) -> Dict[str, Any]:
        """
        Get all information about a product, including its category and features.
        
        Parameters:
        - product_id: ID of the product
        
        Returns:
        - Dictionary containing product information and its relationships
        """
        # Get the product node data
        product_data = self.graph.nodes[product_id]
        
        # Find the category (there should be only one)
        categories = [
            self.graph.nodes[neighbor]['name']
            for neighbor in self.graph.neighbors(product_id)
            if self.graph.nodes[neighbor]['type'] == 'category'
        ]
        
        # Find all features
        features = [
            self.graph.nodes[neighbor]['name']
            for neighbor in self.graph.neighbors(product_id)
            if self.graph.nodes[neighbor]['type'] == 'feature'
        ]
        
        return {
            'product': product_data,
            'category': categories[0] if categories else None,
            'features': features
        }

# Example Usage
def demonstrate_product_catalog():
    """
    This function demonstrates how to use the ProductCatalogGraph class
    with a simple example of a laptop product catalog.
    """
    # Create a new graph
    catalog = ProductCatalogGraph()
    
    # Add categories
    catalog.add_category(
        'cat_laptops',
        'Laptops',
        'Portable computers for work and entertainment'
    )
    
    # Add features
    catalog.add_feature(
        'feat_ssd',
        'SSD Storage',
        'Solid State Drive for fast data access'
    )
    catalog.add_feature(
        'feat_16gb_ram',
        '16GB RAM',
        'High-performance memory for multitasking'
    )
    
    # Add a product
    catalog.add_product(
        'prod_laptop_1',
        'Premium Laptop',
        1299.99,
        'High-performance laptop for professionals'
    )
    
    # Create relationships
    catalog.link_product_to_category('prod_laptop_1', 'cat_laptops')
    catalog.link_product_to_feature('prod_laptop_1', 'feat_ssd')
    catalog.link_product_to_feature('prod_laptop_1', 'feat_16gb_ram')
    
    # Get product information
    laptop_info = catalog.get_product_info('prod_laptop_1')
    print("\nProduct Information:")
    print(f"Name: {laptop_info['product']['name']}")
    print(f"Price: ${laptop_info['product']['price']}")
    print(f"Category: {laptop_info['category']}")
    print("Features:")
    for feature in laptop_info['features']:
        print(f"- {feature}")

if __name__ == "__main__":
    demonstrate_product_catalog() 