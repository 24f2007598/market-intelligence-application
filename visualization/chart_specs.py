from visualization.processors import *

def create_chart_spec(name, chart_type, df, x, y):
    return {
        "chart_title": name,
        "chart_type": chart_type,
        "x_axis_field": x,
        "y_axis_field": y,
        "dataset": df.to_dict(orient="records") if not df.empty else [],
        "labels": {},
        "metadata": {}
    }

def get_executive_specs():
    specs = []
    df1 = process_category_distribution()
    specs.append(create_chart_spec("Category Distribution", "bar", df1, "category", "count"))
    
    df2 = process_change_frequency()
    specs.append(create_chart_spec("Change Frequency Over Time", "line", df2, "date", "count"))
    
    df3 = process_company_activity()
    specs.append(create_chart_spec("Company Activity", "grouped_bar", df3, "company", "count"))
    
    specs.append(create_chart_spec("Change Type Proportions", "pie", df1, "category", "count"))
    return specs

def get_ml_specs():
    specs = []
    df1 = process_dataset_balance()
    specs.append(create_chart_spec("Training Dataset Balance", "bar", df1, "category", "count"))
    
    df2 = process_semantic_similarity()
    specs.append(create_chart_spec("Semantic Similarity Distribution", "histogram", df2, "similarity", None))
    
    df3 = process_chunk_size()
    specs.append(create_chart_spec("Chunk Size Distribution", "histogram", df3, "token_length", None))
    return specs
