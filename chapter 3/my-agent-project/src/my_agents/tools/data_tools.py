def summarize_data(data):
    """Example tool: Summarize a list of numbers."""
    if not data:
        return "No data provided."
    return {
        "count": len(data),
        "min": min(data),
        "max": max(data),
        "average": sum(data) / len(data)
    } 
