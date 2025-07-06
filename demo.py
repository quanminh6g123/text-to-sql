#!/usr/bin/env python3
"""
Text-to-SQL Project Demo Script
This script demonstrates the key capabilities of the project without requiring GPU or model downloads.
"""

import os
import sys
import sqlite3
import pandas as pd
from tabulate import tabulate
import sqlparse
from mschema_implementation import sql_to_mschema

def demo_header():
    """Print a nice header for the demo"""
    print("🗄️ " + "=" * 60)
    print("🗄️  TEXT-TO-SQL PROJECT DEMONSTRATION")
    print("🗄️ " + "=" * 60)
    print()

def demo_mschema_conversion():
    """Demonstrate M-Schema format conversion"""
    print("📋 1. M-SCHEMA FORMAT CONVERSION")
    print("-" * 40)
    
    # Sample database schema
    sample_sql = """
    CREATE TABLE employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary REAL,
        hire_date DATE
    );

    CREATE TABLE departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT,
        manager_id INTEGER,
        FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
    );

    INSERT INTO employees (employee_id, name, department, salary, hire_date) VALUES 
    (1, 'Alice Smith', 'Engineering', 75000, '2023-01-15'),
    (2, 'Bob Johnson', 'Sales', 65000, '2023-02-01'),
    (3, 'Carol Davis', 'Marketing', 70000, '2023-03-10');

    INSERT INTO departments (department_id, department_name, manager_id) VALUES 
    (1, 'Engineering', 1),
    (2, 'Sales', 2),
    (3, 'Marketing', 3);
    """
    
    print("📝 Original SQL Schema:")
    print(sample_sql.strip())
    print()
    
    print("🔄 Converting to M-Schema format...")
    mschema_result = sql_to_mschema(sample_sql, "company_db")
    
    print("✅ M-Schema Result:")
    print(mschema_result)
    print()

def demo_database_creation():
    """Demonstrate in-memory database creation and querying"""
    print("🗄️ 2. IN-MEMORY DATABASE CREATION & QUERYING")
    print("-" * 50)
    
    # Create in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Sample schema and data
    schema_sql = """
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        order_date DATE,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );

    INSERT INTO products VALUES 
    (1, 'Laptop', 'Electronics', 999.99, 50),
    (2, 'Phone', 'Electronics', 599.99, 100),
    (3, 'Desk Chair', 'Furniture', 199.99, 25),
    (4, 'Monitor', 'Electronics', 299.99, 75);

    INSERT INTO orders VALUES 
    (1, 1, 2, '2024-01-15'),
    (2, 2, 1, '2024-01-16'),
    (3, 1, 1, '2024-01-17'),
    (4, 3, 3, '2024-01-18');
    """
    
    print("📝 Creating database schema and inserting data...")
    cursor.executescript(schema_sql)
    
    # Sample queries to demonstrate functionality
    queries = [
        ("📊 All Products", "SELECT * FROM products;"),
        ("💰 Products Over $500", "SELECT product_name, price FROM products WHERE price > 500;"),
        ("📈 Order Summary", """
            SELECT p.product_name, o.quantity, o.order_date 
            FROM orders o 
            JOIN products p ON o.product_id = p.product_id;
        """),
        ("💵 Total Revenue", """
            SELECT SUM(p.price * o.quantity) as total_revenue 
            FROM orders o 
            JOIN products p ON o.product_id = p.product_id;
        """)
    ]
    
    for query_name, query in queries:
        print(f"\n{query_name}:")
        print("SQL:", sqlparse.format(query.strip(), reindent=True, keyword_case='upper'))
        
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        if results:
            df = pd.DataFrame(results, columns=columns)
            print("Results:")
            print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        else:
            print("No results found.")
    
    conn.close()
    print()

def demo_sql_formatting():
    """Demonstrate SQL parsing and formatting"""
    print("🔧 3. SQL PARSING & FORMATTING")
    print("-" * 35)
    
    sample_queries = [
        "select name,salary from employees where department='Engineering' and salary>70000;",
        "SELECT p.product_name,SUM(o.quantity*p.price)as revenue FROM products p JOIN orders o ON p.product_id=o.product_id GROUP BY p.product_name ORDER BY revenue DESC;",
        "INSERT INTO employees(name,department,salary)VALUES('New Employee','HR',55000);"
    ]
    
    for i, query in enumerate(sample_queries, 1):
        print(f"📝 Query {i} (Raw):")
        print(query)
        print()
        
        print(f"✨ Query {i} (Formatted):")
        formatted = sqlparse.format(query, reindent=True, keyword_case='upper')
        print(formatted)
        print("-" * 30)
        print()

def demo_project_capabilities():
    """Show project capabilities and architecture"""
    print("🚀 4. PROJECT CAPABILITIES & FEATURES")
    print("-" * 42)
    
    capabilities = [
        ("🎯 Natural Language to SQL", "Convert questions like 'Show me all employees earning more than $70k' into SQL queries"),
        ("🗄️ In-Memory Database", "Automatically create SQLite databases from schema for query testing"),
        ("▶️ Query Execution", "Run generated SQL queries and display formatted results"),
        ("📊 M-Schema Support", "Convert SQL schemas to M-Schema format for enhanced model training"),
        ("🔧 Model Fine-tuning", "Advanced fine-tuning scripts for XiYanSQL models (3B/32B parameters)"),
        ("🌐 Web Interface", "Modern Gradio-based web UI with responsive design"),
        ("💾 GPU Optimization", "CUDA acceleration with memory monitoring and 4-bit quantization"),
        ("🔒 Security", "Environment-based token management and secure configuration"),
        ("📱 Cross-Platform", "Works on desktop, mobile, and supports Docker deployment"),
        ("⚡ Performance", "Optimized inference with LangChain integration and batch processing")
    ]
    
    for feature, description in capabilities:
        print(f"{feature}")
        print(f"   {description}")
        print()

def demo_architecture():
    """Display project architecture overview"""
    print("🏗️ 5. SYSTEM ARCHITECTURE")
    print("-" * 28)
    
    architecture = """
┌─────────────────────────────────────────────────────────────┐
│                    Text-to-SQL System                       │
├─────────────────────────────────────────────────────────────┤
│  🌐 Frontend Layer                                          │
│  ├── Gradio Web Interface (app_gradio.py)                   │
│  ├── Responsive UI with examples                            │
│  └── Real-time query execution                              │
├─────────────────────────────────────────────────────────────┤
│  🤖 AI/ML Layer                                             │
│  ├── XiYanSQL-QwenCoder Models (3B/32B)                     │
│  ├── LangChain Pipeline Integration                         │
│  ├── HuggingFace Transformers                               │
│  └── GPU-optimized inference                                │
├─────────────────────────────────────────────────────────────┤
│  📊 Data Processing Layer                                   │
│  ├── M-Schema Format Converter                              │
│  ├── SQL DDL Parser                                         │
│  ├── Foreign Key Detection                                  │
│  └── Sample Data Extraction                                 │
├─────────────────────────────────────────────────────────────┤
│  🗄️ Database Layer                                          │
│  ├── In-Memory SQLite Database                              │
│  ├── Schema Validation                                      │
│  ├── Query Execution Engine                                 │
│  └── Results Formatting                                     │
├─────────────────────────────────────────────────────────────┤
│  🔬 Training Infrastructure                                  │
│  ├── Fine-tuning Pipeline (32B models)                      │
│  ├── Unsloth Optimization                                   │
│  ├── 4-bit Quantization                                     │
│  └── Weights & Biases Integration                           │
└─────────────────────────────────────────────────────────────┘
    """
    print(architecture)

def demo_usage_examples():
    """Show typical usage examples"""
    print("💡 6. USAGE EXAMPLES")
    print("-" * 21)
    
    examples = [
        ("Data Analysts", "Generate SQL queries from natural language for business intelligence and reporting"),
        ("Developers", "Rapidly prototype database queries and learn SQL syntax through examples"),
        ("Researchers", "Fine-tune custom models on domain-specific datasets for specialized applications"),
        ("Business Users", "Self-service data access without requiring deep SQL knowledge"),
        ("Database Admins", "Validate query logic and explore database schemas interactively"),
        ("Students", "Learn SQL by seeing how natural language translates to database queries")
    ]
    
    for user_type, use_case in examples:
        print(f"👤 {user_type}:")
        print(f"   {use_case}")
        print()

def main():
    """Run the complete demonstration"""
    demo_header()
    
    try:
        demo_mschema_conversion()
        demo_database_creation()
        demo_sql_formatting()
        demo_project_capabilities()
        demo_architecture()
        demo_usage_examples()
        
        print("✅ " + "=" * 60)
        print("✅  DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("✅ " + "=" * 60)
        print()
        print("🚀 To run the full application:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Set up environment: cp .env.example .env")
        print("   3. Configure Hugging Face token in .env")
        print("   4. Run: python app_gradio.py")
        print()
        print("📚 For more information, see README.md and PROJECT_OVERVIEW.md")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()