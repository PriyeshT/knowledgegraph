# Knowledge Graph RAG System

A powerful system that combines Knowledge Graphs with Retrieval Augmented Generation (RAG) to build intelligent question-answering systems from unstructured text data.

## Features

- **Knowledge Graph Construction**: Automatically builds knowledge graphs from unstructured text
- **Entity Recognition**: Identifies entities (people, organizations, dates, locations, etc.)
- **Relationship Extraction**: Discovers relationships between entities using NLP
- **Semantic Search**: Uses embeddings for intelligent information retrieval
- **Natural Language Answers**: Generates human-readable responses to questions
- **Visualization**: Provides visual representation of the knowledge graph

## Project Structure

```
knowledgegraph/
├── src/
│   ├── core/           # Core knowledge graph functionality
│   ├── examples/       # Example implementations
│   │   └── basic/     # Basic examples
│   └── docs/          # Documentation
│       └── concepts/  # Knowledge graph concepts
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/knowledgegraph.git
cd knowledgegraph
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

### Basic Example

```python
from src.examples.basic.05_rag_with_knowledge_graph import KnowledgeGraphRAG

# Initialize the RAG system
rag = KnowledgeGraphRAG()

# Sample text
text = """
Apple Inc. is a technology company headquartered in Cupertino, California.
Steve Jobs and Steve Wozniak founded Apple in 1976.
The company launched the iPhone in 2007, which revolutionized the smartphone industry.
Tim Cook became CEO in 2011 after Steve Jobs stepped down.
Apple's market value reached $3 trillion in 2022.
"""

# Build the knowledge graph
rag.build_from_text(text)

# Ask questions
questions = [
    "Who founded Apple?",
    "When was the iPhone launched?",
    "What is Apple's market value?",
    "Who is the current CEO of Apple?"
]

for question in questions:
    answer = rag.answer_question(question)
    print(f"Q: {question}")
    print(f"A: {answer}\n")
```

### Running Examples

1. Basic Knowledge Graph:
```bash
python src/examples/basic/01_product_catalog.py
```

2. Complex Knowledge Graph:
```bash
python src/examples/basic/02_complex_product_catalog.py
```

3. Data-Driven Knowledge Graph:
```bash
python src/examples/basic/03_building_from_data.py
```

4. Unstructured Data Processing:
```bash
python src/examples/basic/04_unstructured_data.py
```

5. RAG System:
```bash
python src/examples/basic/05_rag_with_knowledge_graph.py
```

## Dependencies

- networkx==3.2.1: Graph data structure
- matplotlib==3.8.2: Visualization
- graphviz==0.20.1: Graph visualization
- spacy==3.7.2: Natural Language Processing
- sentence-transformers==2.2.2: Text embeddings
- scikit-learn==1.3.2: Machine learning utilities
- huggingface-hub==0.16.4: Model management

## How It Works

1. **Text Processing**:
   - Uses spaCy for entity recognition and relationship extraction
   - Identifies entities (people, organizations, dates, etc.)
   - Extracts relationships between entities

2. **Knowledge Graph Construction**:
   - Creates nodes for entities
   - Creates edges for relationships
   - Stores properties and metadata

3. **Semantic Search**:
   - Generates embeddings for nodes and relationships
   - Uses cosine similarity for semantic matching
   - Finds relevant information for questions

4. **Question Answering**:
   - Identifies relevant nodes and relationships
   - Combines information into coherent answers
   - Provides natural language responses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 