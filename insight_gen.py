import pandas as pd
import json
import numpy as np
# import os
from anthropic import Anthropic
from openai import OpenAI
# import cohere
import json
# from azure.ai.inference import ChatCompletionsClient
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.inference.models import SystemMessage, UserMessage, ChatCompletionsResponseFormat


# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage

# Initialize the Anthropic client
# anthropic = Anthropic(api_key="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")
client = OpenAI(api_key="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")

#co = cohere.Client(api_key="dvuFzrkYtWWqobTrYepzRS1gwqPccS6QjMd9oxyT")

# api_key = "12CxnhIvF4jHuIFwcHAkV72KLWgjeaJM"
# client = MistralClient(api_key=api_key)

# Azure OpenAI Service details

# deployment_name = "cohere-command-r-plus"

# azure_endpoint = "https://cohere-command-r-plus.eastus2.models.ai.azure.com"
# api_key = "FRao4eA6RlOwOOcNyW3lPiNSIAqAGutb"

# # Initialize the client
# model = ChatCompletionsClient(
#     endpoint=azure_endpoint,
#     credential=AzureKeyCredential(api_key),
# )

# def call_azure_openai(prompt):
#     try:
#         response = model.complete(
#             messages=[
#                 SystemMessage(content="You are a helpful assistant."),
#                 UserMessage(content=prompt),
#             ],
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         raise Exception(f"Azure AI Model Inference API call failed: {str(e)}")
 
def summarize_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)
    
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    json_output = {}
    for column in df.columns:
        samples = df[column].dropna().unique()[:3]
        samples = [sample.item() if isinstance(sample, np.int64) else str(sample) if isinstance(sample, pd.Timestamp) else sample for sample in samples]
        json_output[column] = {
            "dtype": str(df[column].dtype),
            "samples": samples
        }

    return json_output

def generate_code(summary, query):
    prompt = f"""You are a Python expert. Generate Python code for the following query.
    
    Query: {query}
    
    CSV Summary: {json.dumps(summary, indent=2)}

    First understand the query given correctly.

    Always check that if the characters of column names and its values given in the query do not match the case (UpperCase or Lowercase) of the DataFrame column names and its values, then make the changes accordingly so that it matches the column name and its values in the DataFrame, and then generate the Python code.
    Assume the DataFrame 'df' is already loaded.
    Do not use aggregate functions on columns with dtype:"object".
    
    Save the final result in 'result'. It should contain all the relevant information like, all the required columns to generate insight out of it. If 'result' variable holds a single value then first convert it into a DataFrame.
    
    Review the generated code to ensure it is correct and adequately answers the query. If the result is incorrect or insufficient, rewrite the code to address the issues. Repeat this process until the result is correct.
    
    Never display result e.g., print(result)."""

    # message = anthropic.messages.create(
    #     model= "claude-3-5-sonnet-20240620",
    #     max_tokens=1000,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # )
    
    # generated_text = message.content[0].text
    

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
        
        {"role": "user", "content": prompt}
        ]
        
    )

    generated_text = response.choices[0].message.content.strip()

    # chat_response = client.chat(
    #     model="codestral-latest",
    #     max_tokens=1000,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # )
    
    # generated_text = chat_response.choices[0].message.content.strip()

    # response = co.chat(
    #    model="command-r-plus",
    #    message= prompt
    # )

    # generated_text = response.text.strip()


    # generated_text = call_azure_openai(prompt)

    # Extract the Python code from the response
    code_start = generated_text.find("```python")
    code_end = generated_text.rfind("```")

    if code_start != -1 and code_end != -1:
        # Extract the code between the triple backticks
        generated_code = generated_text[code_start + len("```python"):code_end].strip()
    else:
        # If no triple backticks are found, return the entire response
        generated_code = generated_text.strip()
        
    print("Generated Code:", generated_code)
    return generated_code

def normalize_query_case(query, df):
    """
    Normalize the case of the query to match the DataFrame's columns and values.
    """
    query_lower = query.lower()
    column_names = df.columns.str.lower()

    # Replace column names in the query with the correct case from the DataFrame
    for col in column_names:
        query_lower = query_lower.replace(col.lower(), df.columns[column_names.tolist().index(col)])
    
    # Handle values normalization: This requires knowing which columns are being queried and what values
    for col in df.columns:
        if df[col].dtype == 'object':
            unique_values = df[col].unique()
            for val in unique_values:
                if isinstance(val, str) and val.lower() in query_lower:
                    query_lower = query_lower.replace(val.lower(), val)
    
    return query_lower



def generate_insights(output, query):
    prompt = f"""You are an AI assistant proficient in generating Highcharts visualizations and an insightful data analyst. Given the following data, generate descriptive insights about the data in natural language answering the query asked. Assume that the user will only be looking at the response generated and not the original dataframe.
    Always analyze the complete output carefully before generating insights and do not leave any column and any important insight from the output.

    Ensure to provide a detailed description of the results, making sure to consider all columns and their potential impact. Highlight any patterns, trends, or significant values.
    
    Assume when recommending chart type that only 'highcharts' library is available so, only recommend supported charts that can provide some extra insights into the data than other previosly recommended charts, details should not be same for any chart and they should provide best help to visualize the respective insight and try to provide varied chart types, if any.
    Generate a Highcharts configuration for visualizing data. Please create charts that are more complex and varied than basic bar, scatter or pie charts. 
    Include examples such as spline, area, heatmap, bubble or combination charts or many more.

    You must answer the query asked and do not skip any information in response.Return your response as a JSON object with the following structure:
    {{
    
       "Insight_1": {{
          "title": "The specific and descriptive title for the insight telling something specific about that insight",   
          "description": "Insight should be here",
          "requireChart": "'true' or 'false' depending, if a chart is required to give value to this insight",
          "details": {
                "This object should contain all the necessary settings and data to define and render a specific highchart chart in format that it accepts the title text should be based on the chart"
          }
        }},
        "Insight_2": {{...}}
        ...
        "Insight_N": {{...}}
    }}

    Data: {output}

    Query: {query}
    
    Provide the insights in a detailed and clear manner.
    """

    # message = anthropic.messages.create(
    #     model= "claude-3-5-sonnet-20240620",
    #     max_tokens=1500,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # )
    
    # insights = message.content[0].text

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
        
        {"role": "user", "content": prompt}
        ],

        response_format={"type": "json_object"}
        
    )
    insights = response.choices[0].message.content.strip()

    # chat_response = client.chat(
    #     model="mistral-large-latest",
    #     max_tokens=2000,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ],
    #     response_format={"type": "json_object"}
    # )
    
    # insights = chat_response.choices[0].message.content

    # response = co.chat(
    #    model="command-r-plus",
    #    message= prompt
    # )

    # insights = response.text.strip()
    # print(insights)

    # insights = response.choices[0].message.content
    
    
    
    try:
        insights = json.loads(insights)
        return insights
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None

   
    

   
    # insights = call_azure_openai(prompt)

    # Extract the Python code from the response
    # code_start = insights.find("json")
    # code_end = insights.rfind("")

    # if code_start != -1 and code_end != -1:
    #     # Extract the code between the triple backticks
    #     insights = insights[code_start + len("json"):code_end].strip()
    # else:
    #     # If no triple backticks are found, return the entire response
    #     insights = insights.strip()
    
    # try:
    #     insights_json = json.loads(insights)
    #     return insights_json
    # except json.JSONDecodeError:
    #     print("Error: The response from Azure AI is not in valid JSON format.")
    #     return None

def save_and_execute_generated_code(generated_code, csv_file_path, query):
    file_path = "GenCode.py"
    with open(file_path, 'w') as file:
        file.write(f"import pandas as pd\n")
        file.write(f"import numpy as np\n\n")
        file.write(f"csv_file_path = '{csv_file_path}'\n")
        file.write(f"df = pd.read_csv(csv_file_path)\n\n")
        
        # Clean the DataFrame by removing leading/trailing whitespaces from string columns
        file.write(f"for column in df.columns:\n")
        file.write(f"    if df[column].dtype == 'object':\n")
        file.write(f"        df[column] = df[column].apply(lambda x: x.strip() if isinstance(x, str) else x)\n\n")
        
        # Ensure 'DateKey' column is parsed as datetime
        file.write(f"if 'DateKey' in df.columns:\n")
        file.write(f"    df['DateKey'] = pd.to_datetime(df['DateKey'], errors='coerce')\n\n")
        
        file.write(f"# Query: {query}\n")
        file.write(generated_code + "\n\n")
        file.write(f"# Save result to a temporary CSV file\n")
        file.write(f"result.to_csv('result.csv', index=False)\n")
        

    print(f"Generated code has been saved to {file_path}")

    try:
        exec(open(file_path).read())
        with open('result.csv', 'r') as f:
            output = f.read()
        print(output)
        return output
    except Exception as e:
        print(f"Error executing generated code:\n{str(e)}")
        return None

def auto_generate_df(summary, query, csv_file_path, df):
    if(query):
       normalized_query = normalize_query_case(query, df)
       while True:
          generated_code = generate_code(summary, normalized_query)
          output = save_and_execute_generated_code(generated_code, csv_file_path, query)
          if output:
              data = pd.read_csv("result.csv")
              return data


# Re-load the CSV file once
def insight(query):
    csv_file_path = "Retail.csv"
    df = pd.read_csv(csv_file_path)
    summary = summarize_csv(csv_file_path)
    print("\nCSV Summary:\n", json.dumps(summary, indent=2))

    while True:
        output_df = auto_generate_df(summary, query, csv_file_path, df)
        if output_df is not None:
            response = generate_insights(output_df, query)
            #print("\nGenerated Insights:\n", response)
            return response
        
        
def validate_chart_config(insight):
    if insight.get('requireChart') == 'true' and 'details' in insight:
        # Add checks for required chart properties
        required_props = ['chart', 'series', 'title']
        for prop in required_props:
            if prop not in insight['details']:
                print(f"Warning: Missing {prop} in chart configuration")
                return False
    return True


        #charts_created= auto_generate_chart(output_df, response)