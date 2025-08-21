import pandas as pd
import os

class AnalysisTool:
    def __init__(self):
        self.name = "AnalysisTool"
        self.description = "A tool for performing data analysis, especially on structured data like CSV files."

    def analyze_csv(self, file_path: str):
        """
        Analyzes a CSV file and returns key insights.
        Parameters:
            file_path (str): The absolute path to the CSV file.
        """
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        
        try:
            df = pd.read_csv(file_path)
            
            summary = f"Analysis of {os.path.basename(file_path)}:\n"
            summary += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
            
            # Basic numerical column summary
            numerical_cols = df.select_dtypes(include=['number']).columns
            if not numerical_cols.empty:
                summary += "\nNumerical Column Summary:\n"
                summary += df[numerical_cols].describe().to_string() + "\n"
            
            # Basic categorical column summary
            categorical_cols = df.select_dtypes(include=['object']).columns
            if not categorical_cols.empty:
                summary += "\nCategorical Column Value Counts (Top 5):\n"
                for col in categorical_cols:
                    summary += f"- {col}:\n"
                    summary += df[col].value_counts().head(5).to_string() + "\n"
            
            return summary
        except Exception as e:
            return f"Error analyzing CSV file: {e}"