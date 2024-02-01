import os
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon, shapiro


#This method accepts the original survey results file in CSV format,
#converts the Likert results to numerical values,
#creates a median value for each question for all the respondents,
#writes the medians to a file
def process_likert_scale_responses(input_file_path, output_file_path):
    # Read the CSV file, specifying the first row as header
    data = pd.read_csv(input_file_path, header=0)

    # Mapping for Likert scale
    likert_mapping = {
        'Strongly Disagree': 1,
        'Disagree': 2,
        'Neutral': 3,
        'Agree': 4,
        'Strongly Agree': 5,
        'N/A': 0,
        'NaN': 0  # To handle any NaN values
    }

    # Identify columns that start with "Question"
    question_columns = [col for col in data.columns if col.startswith('Question')]

    # Iterate through each column and apply the mapping where applicable
    for column in question_columns:
        if data[column].dtype == 'object':  # Checking if the column has object (string) type
            # Replace values based on mapping
            #data[column] = data[column].replace(likert_mapping)
            data[column] = data[column].replace(likert_mapping).infer_objects(copy=False)

    # Replace 'NaN' with 0 in these columns
    data[question_columns] = data[question_columns].fillna(0)

    # Calculating the median for each numeric column and rounding it
    median_data = data[question_columns].median(numeric_only=True).round()

    # Creating a new dataframe with the rounded median data
    result_df = pd.DataFrame([median_data], index=['Median'])

    # Add empty columns for those that do not start with "Question"
    non_question_columns = [col for col in data.columns if not col.startswith('Question')]
    for column in non_question_columns:
        result_df[column] = np.nan

    # Reorder columns to match the original dataframe
    result_df = result_df[data.columns]

    # Writing the median data to a new CSV file
    result_df.to_csv(output_file_path, index=False)

    return output_file_path

#The median of the results from every respondent is calculated previously and passed as input to this step.
#Process survey results for each survey i.e. PGx AI Assistant Provider and Patient and ChatGPT Provider and Patient
#into counts for each Likert scale and rubric category
def process_and_visualize_data(input_file_path, output_file_path, aggregate_output_file_path, file_type):
    # Load the CSV file
    df_modified = pd.read_csv(input_file_path)

    # Create a mapping of questions to sections
    question_to_section = {}
    for col in df_modified.columns:
        if col.startswith("Section"):
            section = col
        elif col.startswith("Question"):
            question_to_section[col] = section

    # We need to identify the question columns
    question_columns_modified = [col for col in df_modified.columns if col.startswith("Question")]

    # Melt only the question columns
    melted_df_modified = df_modified[question_columns_modified].melt(var_name="Question", value_name="Response")

    # Map each question to its section
    melted_df_modified['Section'] = melted_df_modified['Question'].map(question_to_section)

    # Define rubric categories based on file type
    if file_type == "patient":
        rubric_categories = {'Responses are accurate': 'Accuracy', 'Responses are relevant': 'Relevancy',
                             'Language is clear, accessible & empathetic': 'Language', 'Responses are unbiased': 'Bias',
                             'Responses minimize risk': 'Risk', 'Responses are free of hallucinations': 'Hallucination'}
    elif file_type == "provider":
        rubric_categories = {'Responses are accurate': 'Accuracy', 'Responses are relevant': 'Relevancy',
                             'Language is clear & accessible': 'Language', 'Responses minimize risk': 'Risk',
                             'Responses are well cited & referenced': 'Citations',
                             'Responses are free of hallucinations': 'Hallucination'}

    # Add a 'Rubric Category' column based on whether the 'Question' column contains each rubric category
    for category, short_form in rubric_categories.items():
        melted_df_modified.loc[melted_df_modified['Question'].str.contains(category), 'Rubric Category'] = short_form

    # Remove the rubric category from the 'Question' column
    melted_df_modified['Question'] = melted_df_modified['Question'].str.replace(r'[.*]', '')

    # Drop rows with 'nan' in 'Section' or 'Rubric Category' column
    melted_df_modified = melted_df_modified.dropna(subset=['Section', 'Rubric Category'])

    # Group by 'Section', 'Rubric Category', and 'Response'
    section_grouped_modified = melted_df_modified.groupby(['Section', 'Rubric Category', 'Response']).size()
    print("Unique response categories in the data:", melted_df_modified['Response'].unique())

    # Define the order of the responses
    response_order = melted_df_modified['Response'].unique()

    # Reindex the grouped DataFrame to ensure all response categories are present in every row
    section_grouped_modified = section_grouped_modified.unstack().reindex(columns=response_order, fill_value=0)

    # Extract the question number from the 'Question' column
    melted_df_modified['Question Number'] = melted_df_modified['Question'].str.extract(r'(Question \d+)')

    # Write the section data to a CSV file.
    output_file = os.path.join(output_file_path)
    section_grouped_modified.to_csv(output_file)

    # Append the aggregate data to the same CSV file.
    aggregate_data = section_grouped_modified.groupby(
        level='Rubric Category').sum()  # Aggregate data by summing over all sections
    aggregate_data.index = pd.MultiIndex.from_product([['Overall'], aggregate_data.index])
    aggregate_data.to_csv(output_file, mode='a', header=False)

    # Write the aggregate data to another CSV file.
    aggregate_output_file = os.path.join(aggregate_output_file_path)
    aggregate_data.reset_index().to_csv(aggregate_output_file, index=False)  # Reset index before writing to file


#This method compares the pgx ai assitant to chatgpt and
#calculates p value and effect size
def calculate_wilcoxon_and_effect_size(file1, file2, output_file_path):
    # Read the median files
    data1 = pd.read_csv(file1)
    data2 = pd.read_csv(file2)

    # Filter columns that start with 'Question'
    question_columns1 = [col for col in data1.columns if col.startswith('Question')]
    question_columns2 = [col for col in data2.columns if col.startswith('Question')]

    # Rename 'Question' columns with unique numbers in the format 'Q1', 'Q2', 'Q3', etc.
    rename_dict1 = {col: f'Q{i+1}' for i, col in enumerate(question_columns1)}
    rename_dict2 = {col: f'Q{i+1}' for i, col in enumerate(question_columns2)}
    data1.rename(columns=rename_dict1, inplace=True)
    data2.rename(columns=rename_dict2, inplace=True)

    # Select only the renamed 'Question' columns
    data1 = data1[rename_dict1.values()]
    data2 = data2[rename_dict2.values()]

    # Write the modified data to new CSV files
    #data1.to_csv(file1.replace('.csv', '_modified.csv'), index=False)
    #data2.to_csv(file2.replace('.csv', '_modified.csv'), index=False)

    # Ensure that the data are paired correctly
    assert (data1.columns == data2.columns).all(), "Headers must be in the same order in both files"

    # Perform the Wilcoxon signed-rank test
    stat, p = wilcoxon(data1.iloc[0], data2.iloc[0])

    # Convert two-tailed p-value to one-tailed (since we have a specific direction in mind)
    p_one_tailed = p / 2

    # Calculate Cohen's d
    mean1 = np.mean(data1.iloc[0])
    mean2 = np.mean(data2.iloc[0])
    std1 = np.std(data1.iloc[0], ddof=1)  # ddof=1 to use the unbiased estimator (n-1 in the denominator)
    std2 = np.std(data2.iloc[0], ddof=1)
    pooled_std = np.sqrt((std1 ** 2 + std2 ** 2) / 2)
    cohen_d = (mean1 - mean2) / pooled_std

    # Assume `data` is a one-dimensional NumPy array or a Pandas Series
    stat, p = shapiro(data1)

    print(f"Shapiro-Wilk Test statistic: {stat}")
    print(f"p-value: {p}")
    # Create a DataFrame with the results
    results_df = pd.DataFrame({
        'Statistic': [stat],
        'p-value': [p_one_tailed],
        "Cohen's d": [cohen_d]
    })

    # Write the results to a CSV file
    results_df.to_csv(output_file_path, index=False)

    return stat, p_one_tailed, cohen_d


def compare_ai_performance(chatgpt_file, pgx_file, output_file):
    # Load data from CSV files
    chatgpt_df = pd.read_csv(chatgpt_file)
    pgx_df = pd.read_csv(pgx_file)

    # Remove the 'level_0' column if it exists
    if 'level_0' in chatgpt_df.columns:
        chatgpt_df = chatgpt_df.drop(columns=['level_0'])
    if 'level_0' in pgx_df.columns:
        pgx_df = pgx_df.drop(columns=['level_0'])

    # Remove leading/trailing whitespaces from column names
    chatgpt_df.columns = chatgpt_df.columns.str.strip()
    pgx_df.columns = pgx_df.columns.str.strip()

    # Set 'Category' as index
    chatgpt_df.set_index('Rubric Category', inplace=True)
    pgx_df.set_index('Rubric Category', inplace=True)

    # Assign weights and calculate weighted score
    #weights = {'Strongly Agree': 5, 'Agree': 4, 'Neutral': 3, 'Disagree': 2, 'Strongly Disagree': 1, 'NA':0}
    #print(chatgpt_df.columns)
    #chatgpt_score = chatgpt_df.mul([weights[key] for key in chatgpt_df.columns], axis=1).sum(axis=1)
    #pgx_score = pgx_df.mul([weights[key] for key in pgx_df.columns], axis=1).sum(axis=1)

    # Convert column names to floats
    chatgpt_df.columns = chatgpt_df.columns.astype(float)
    pgx_df.columns = pgx_df.columns.astype(float)

    # Assign weights and calculate weighted score
    weights = {5.0: 5, 4.0: 4, 3.0: 3, 2.0: 2, 1.0: 1, 0.0: 0}
    chatgpt_score = chatgpt_df.mul([weights[key] for key in chatgpt_df.columns], axis=1).sum(axis=1)
    pgx_score = pgx_df.mul([weights[key] for key in pgx_df.columns], axis=1).sum(axis=1)

    # Calculate the total possible score for each category
    total_possible_score = chatgpt_df.sum(axis=1) * 5  # Number of responses times maximum weight of 5

    # Convert scores to percentage
    chatgpt_percentage = (chatgpt_score / total_possible_score) * 100
    pgx_percentage = (pgx_score / total_possible_score) * 100

    # Calculate overall scores
    overall_chatgpt_score = chatgpt_score.sum()
    overall_pgx_score = pgx_score.sum()
    overall_possible_score = total_possible_score.sum()
    overall_chatgpt_percentage = (overall_chatgpt_score / overall_possible_score) * 100
    overall_pgx_percentage = (overall_pgx_score / overall_possible_score) * 100

    percentage_df = pd.DataFrame({'ChatGPT': chatgpt_percentage, 'PGx AI Assistant': pgx_percentage})
    overall_df = pd.DataFrame({'ChatGPT': [overall_chatgpt_percentage], 'PGx AI Assistant': [overall_pgx_percentage]}, index=['Overall'])

    # Append overall scores to the dataframe
    percentage_df = pd.concat([percentage_df, overall_df])

    # Round off the percentages to nearest whole number
    #percentage_df = percentage_df.round(0).astype(int)
    percentage_df = np.rint(percentage_df).astype(int)
    # Write the results to a CSV file
    percentage_df.to_csv(output_file)
    '''
    # Create a bar plot
    ax = percentage_df.plot(kind='bar', figsize=(10, 6))
    plt.title('Comparison of ChatGPT and PGx AI Assistant')
    plt.ylabel('Performance (%)')

    # Display the percentage at the end of each bar
    for p in ax.patches:
        ax.annotate(str(p.get_height()) + '%', (p.get_x() * 1.005, p.get_height() * 1.005))

    plt.show()
    '''

#Provider Version - Process Likert Scale Responses from all survey respondents to a Median Value and write to output file
chatgptprovider_input_file_path = 'inputfiles/ChatGPT 3.5 PGx Responses - Provider Evaluation.csv'
pgxprovider_input_file_path = 'inputfiles/Pharmacogenetics (PGx) AI Assistant - Provider Evaluation.csv'
chatgptprovider_output_file_path = 'outputfiles/provider/Median_ChatGPT 3.5 PGx Responses - Provider Evaluation.csv'
pgxprovider_output_file_path = 'outputfiles/provider/Median_Pharmacogenetics (PGx) AI Assistant - Provider Evaluation.csv'
process_likert_scale_responses(pgxprovider_input_file_path, pgxprovider_output_file_path)
process_likert_scale_responses(chatgptprovider_input_file_path, chatgptprovider_output_file_path)

#Patient Version - Process Likert Scale Responses from all survey respondents to a Median Value and write to output file
chatgptpatient_input_file_path = 'inputfiles/ChatGPT 3.5 PGx Responses - Patient Evaluation.csv'
pgxpatient_input_file_path = 'inputfiles/Pharmacogenetics (PGx) AI Assistant - Patient Evaluation.csv'
chatgptpatient_output_file_path = 'outputfiles/patient/Median_ChatGPT 3.5 PGx Responses - Patient Evaluation.csv'
pgxpatient_output_file_path = 'outputfiles/patient/Median_Pharmacogenetics (PGx) AI Assistant - Patient Evaluation.csv'
process_likert_scale_responses(pgxpatient_input_file_path, pgxpatient_output_file_path)
process_likert_scale_responses(chatgptpatient_input_file_path, chatgptpatient_output_file_path)

#These methods below calculate the frequency of the responses for every category i.e. the number of 'Strongly Agree(5)', 'Agree(4)', 'Neutral(3)', 'Disagree(2)', 'Strongly Disagree(1)'
# for each section and an overall aggregate by category for each of the four surveys. These results are then output to the respective 'Summation*.csv' files.
process_and_visualize_data(pgxprovider_output_file_path, 'outputfiles/provider/Summation_Pharmacogenetics (PGx) AI Assistant - Provider Evaluation.csv','outputfiles/provider/Overall_Pharmacogenetics (PGx) AI Assistant - Provider Evaluation.csv','provider')
process_and_visualize_data(chatgptprovider_output_file_path, 'outputfiles/provider/Summation_ChatGPT 3.5 PGx Responses - Provider Evaluation.csv','outputfiles/provider/Overall_ChatGPT 3.5 PGx Responses - Provider Evaluation.csv','provider')
process_and_visualize_data(pgxpatient_output_file_path, 'outputfiles/patient/Summation_Pharmacogenetics (PGx) AI Assistant - Patient Evaluation.csv','outputfiles/patient/Overall_Pharmacogenetics (PGx) AI Assistant - Patient Evaluation.csv','patient')
process_and_visualize_data(chatgptpatient_output_file_path, 'outputfiles/patient/Summation_ChatGPT 3.5 PGx Responses - Patient Evaluation.csv','outputfiles/patient/Overall_ChatGPT 3.5 PGx Responses - Patient Evaluation.csv','patient')

#Compute Wilcoxon Signed Rank Test statistics i.e. p-value and effect size comparing chatgpt and pgx ai assistant for patient and provider
output_file_path_provider = 'outputfiles/provider/Wilcoxon_Results.csv'
output_file_path_patient = 'outputfiles/patient/Wilcoxon_Results.csv'
stat, p, cohen_d = calculate_wilcoxon_and_effect_size(pgxprovider_output_file_path, chatgptprovider_output_file_path, output_file_path_provider)
print(f"Wilcoxon Signed-Rank Test statistic for provider: {stat}")
print(f"p-value for provider: {p}")
print(f"Effect size for provider: {cohen_d}")

stat, p, cohen_d = calculate_wilcoxon_and_effect_size(pgxpatient_output_file_path, chatgptpatient_output_file_path, output_file_path_patient)
print(f"Wilcoxon Signed-Rank Test statistic for patient: {stat}")
print(f"p-value for patient: {p}")
print(f"Effect size for patient: {cohen_d}")

# Compare AI performance between chatgpt and pgx for patient and provider respectively
compare_ai_performance('outputfiles/provider/Overall_ChatGPT 3.5 PGx Responses - Provider Evaluation.csv',
                       'outputfiles/provider/Overall_Pharmacogenetics (PGx) AI Assistant - Provider Evaluation.csv',
                       'outputfiles/provider/Comparison_Results Provider.csv')
compare_ai_performance('outputfiles/patient/Overall_ChatGPT 3.5 PGx Responses - Patient Evaluation.csv',
                       'outputfiles/patient/Overall_Pharmacogenetics (PGx) AI Assistant - Patient Evaluation.csv',
                       'outputfiles/patient/Comparison_Results Patient.csv')


#Finally, combine all csvs into one excel file for patient and provider respectively
def write_to_excel(file_paths, output_file_path):
    with pd.ExcelWriter(output_file_path) as writer:
        for file_path in file_paths:
            df = pd.read_csv(file_path)
            # Limit the sheet name to 30 characters
            sheet_name = os.path.basename(file_path).replace('.csv', '')[:30]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
# Define the input and output file paths
input_file_paths_provider = [
    'outputfiles/provider/Summation_Pharmacogenetics (PGx) AI Assistant - Provider Evaluation.csv',
    'outputfiles/provider/Overall_Pharmacogenetics (PGx) AI Assistant - Provider Evaluation.csv',
    'outputfiles/provider/Summation_ChatGPT 3.5 PGx Responses - Provider Evaluation.csv',
    'outputfiles/provider/Overall_ChatGPT 3.5 PGx Responses - Provider Evaluation.csv',
    'outputfiles/provider/Comparison_Results Provider.csv',
    'outputfiles/provider/Wilcoxon_Results.csv'
]
output_file_path_provider = 'outputfiles/Provider_Results.xlsx'

input_file_paths_patient = [
    'outputfiles/patient/Summation_Pharmacogenetics (PGx) AI Assistant - Patient Evaluation.csv',
    'outputfiles/patient/Overall_Pharmacogenetics (PGx) AI Assistant - Patient Evaluation.csv',
    'outputfiles/patient/Summation_ChatGPT 3.5 PGx Responses - Patient Evaluation.csv',
    'outputfiles/patient/Overall_ChatGPT 3.5 PGx Responses - Patient Evaluation.csv',
    'outputfiles/patient/Comparison_Results Patient.csv',
    'outputfiles/patient/Wilcoxon_Results.csv'
]
output_file_path_patient = 'outputfiles/Patient_Results.xlsx'

# Write the results to Excel files
write_to_excel(input_file_paths_provider, output_file_path_provider)
write_to_excel(input_file_paths_patient, output_file_path_patient)