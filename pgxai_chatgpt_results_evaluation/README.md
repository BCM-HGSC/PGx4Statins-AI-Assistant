#### Overview:
This folder contains the code and data used for evaluating the performance of the PGx AI assistant, both as a standalone entity and in comparison with OpenAI's ChatGPT 3.5, leveraging data derived from evaluation surveys conducted by an expert panel. 
##### Code:
The script results.py processes survey data, including transforming Likert scale responses to numerical values, calculating median responses for consensus, generating frequency distributions for each criterion, and determining weighted performance scores and statistical significance for both the AI Assistant and ChatGPT 3.5.
##### Survey Results (Input Files): 
Raw data files representing the responses collected from the expert panel, structured according to a series of predefined criteria based on the Likert scale.
##### Processed Outputs (Output Files):
Frequency Distribution: Shows aggregated responses for each Likert scale category across evaluation criteria, displaying expert opinion distribution.
Weighted Performance Scores: Scores for each criterion, derived by weighting Likert scale responses and converting these to percentages based on the maximum possible score.
Comparative Analysis and Visualization Plots: Includes graphs for a visual comparison of weighted performance scores between the AI Assistant and ChatGPT 3.5, offering clear insights into their respective performances.
