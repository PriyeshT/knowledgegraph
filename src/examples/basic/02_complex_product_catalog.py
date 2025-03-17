"""
Complex Product Catalog Knowledge Graph Example
--------------------------------------------
This example demonstrates a more realistic product catalog with:
1. Multiple products across different categories
2. Shared features between products
3. Visualization of the knowledge graph
4. Advanced querying capabilities
"""

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Set
from collections import defaultdict

class EnhancedProductCatalog:
    def __init__(self):
        """Initialize an empty knowledge graph with enhanced capabilities."""
        self.graph = nx.Graph()
        
    def add_product(self, product_id: str, name: str, price: float, description: str) -> None:
        """Add a product to the graph with enhanced properties."""
        self.graph.add_node(
            product_id,
            type='product',
            name=name,
            price=price,
            description=description,
            color='lightblue'  # For visualization
        )
    
    def add_category(self, category_id: str, name: str, description: str) -> None:
        """Add a product category to the graph."""
        self.graph.add_node(
            category_id,
            type='category',
            name=name,
            description=description,
            color='lightgreen'  # For visualization
        )
    
    def add_feature(self, feature_id: str, name: str, description: str) -> None:
        """Add a product feature to the graph."""
        self.graph.add_node(
            feature_id,
            type='feature',
            name=name,
            description=description,
            color='lightpink'  # For visualization
        )
    
    def link_product_to_category(self, product_id: str, category_id: str) -> None:
        """Create a relationship between a product and its category."""
        self.graph.add_edge(
            product_id,
            category_id,
            relationship_type='belongs_to',
            color='blue'  # For visualization
        )
    
    def link_product_to_feature(self, product_id: str, feature_id: str) -> None:
        """Create a relationship between a product and its features."""
        self.graph.add_edge(
            product_id,
            feature_id,
            relationship_type='has_feature',
            color='red'  # For visualization
        )
    
    def get_products_by_feature(self, feature_name: str) -> List[Dict[str, Any]]:
        """
        Find all products that have a specific feature.
        
        Parameters:
        - feature_name: Name of the feature to search for
        
        Returns:
        - List of products with the specified feature
        """
        products = []
        for node in self.graph.nodes():
            if self.graph.nodes[node]['type'] == 'feature' and self.graph.nodes[node]['name'] == feature_name:
                # Get all connected products
                for neighbor in self.graph.neighbors(node):
                    if self.graph.nodes[neighbor]['type'] == 'product':
                        products.append(self.get_product_info(neighbor))
        return products
    
    def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Dict[str, Any]]:
        """
        Find all products within a specific price range.
        
        Parameters:
        - min_price: Minimum price
        - max_price: Maximum price
        
        Returns:
        - List of products within the price range
        """
        products = []
        for node in self.graph.nodes():
            if self.graph.nodes[node]['type'] == 'product':
                price = self.graph.nodes[node]['price']
                if min_price <= price <= max_price:
                    products.append(self.get_product_info(node))
        return products
    
    def get_product_info(self, product_id: str) -> Dict[str, Any]:
        """Get all information about a product, including its category and features."""
        product_data = self.graph.nodes[product_id]
        
        categories = [
            self.graph.nodes[neighbor]['name']
            for neighbor in self.graph.neighbors(product_id)
            if self.graph.nodes[neighbor]['type'] == 'category'
        ]
        
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
    
    def visualize_graph(self, title: str = "Product Catalog Knowledge Graph") -> None:
        """
        Visualize the knowledge graph using matplotlib.
        
        Parameters:
        - title: Title for the visualization
        """
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

def demonstrate_complex_catalog():
    """Demonstrate the enhanced product catalog with multiple products and visualization."""
    # Create a new graph
    catalog = EnhancedProductCatalog()
    
    # Add categories
    categories = {
        'cat_laptops': ('Laptops', 'Portable computers for work and entertainment'),
        'cat_phones': ('Smartphones', 'Mobile devices for communication and apps'),
        'cat_tablets': ('Tablets', 'Portable touch-screen devices')
    }
    
    for cat_id, (name, desc) in categories.items():
        catalog.add_category(cat_id, name, desc)
    
    # Add features
    features = {
        'feat_ssd': ('SSD Storage', 'Solid State Drive for fast data access'),
        'feat_16gb_ram': ('16GB RAM', 'High-performance memory for multitasking'),
        'feat_5g': ('5G Connectivity', 'Next-generation wireless technology'),
        'feat_oled': ('OLED Display', 'High-quality organic light-emitting diode screen'),
        'feat_8gb_ram': ('8GB RAM', 'Standard memory for everyday use')
    }
    
    for feat_id, (name, desc) in features.items():
        catalog.add_feature(feat_id, name, desc)
    
    # Add products
    products = [
        ('prod_laptop_1', 'Premium Laptop', 1299.99, 'High-performance laptop for professionals'),
        ('prod_laptop_2', 'Budget Laptop', 599.99, 'Affordable laptop for everyday use'),
        ('prod_phone_1', 'Flagship Phone', 999.99, 'Top-tier smartphone with latest features'),
        ('prod_phone_2', 'Mid-range Phone', 499.99, 'Balanced smartphone for most users'),
        ('prod_tablet_1', 'Pro Tablet', 799.99, 'Professional tablet for creative work')
    ]
    
    for prod_id, name, price, desc in products:
        catalog.add_product(prod_id, name, price, desc)
    
    # Create relationships
    relationships = [
        # Laptop relationships
        ('prod_laptop_1', 'cat_laptops', ['feat_ssd', 'feat_16gb_ram']),
        ('prod_laptop_2', 'cat_laptops', ['feat_8gb_ram']),
        
        # Phone relationships
        ('prod_phone_1', 'cat_phones', ['feat_5g', 'feat_oled']),
        ('prod_phone_2', 'cat_phones', ['feat_5g']),
        
        # Tablet relationships
        ('prod_tablet_1', 'cat_tablets', ['feat_oled', 'feat_8gb_ram'])
    ]
    
    for prod_id, cat_id, feat_ids in relationships:
        catalog.link_product_to_category(prod_id, cat_id)
        for feat_id in feat_ids:
            catalog.link_product_to_feature(prod_id, feat_id)
    
    # Visualize the graph
    catalog.visualize_graph()
    
    # Demonstrate queries
    print("\nProducts with SSD Storage:")
    ssd_products = catalog.get_products_by_feature('SSD Storage')
    for product in ssd_products:
        print(f"- {product['product']['name']} (${product['product']['price']})")
    
    print("\nProducts between $500 and $1000:")
    price_range_products = catalog.get_products_by_price_range(500, 1000)
    for product in price_range_products:
        print(f"- {product['product']['name']} (${product['product']['price']})")

if __name__ == "__main__":
    demonstrate_complex_catalog() 