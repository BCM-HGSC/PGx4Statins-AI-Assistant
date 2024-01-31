import docx
import nltk
import pyphen
import os
def evaluate_readability(file_path, start_text):
    # Load the document
    doc = docx.Document(file_path)

    # Join all paragraphs into a single string
    all_text = ' '.join([para.text for para in doc.paragraphs])

    # Split the text by start_text
    parts = all_text.split(start_text)[1:]  # Skip the first part as it's before the first start_text

    # Extract the text before 'Mark only one oval per row.' for each part
    text = ' '.join([part[:part.find('Mark only one oval per row.')] for part in parts if 'Mark only one oval per row.' in part])

    # Split the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Initialize counters
    num_words = 0
    num_syllables = 0
    num_polysyllable_words = 0

    # Create a Pyphen object for counting syllables
    dic = pyphen.Pyphen(lang='en')

    # For each sentence, split it into words and count the number of words and syllables
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        num_words += len(words)
        num_syllables += sum([len(dic.inserted(word).split('-')) for word in words])
        num_polysyllable_words += sum([1 for word in words if len(dic.inserted(word).split('-')) >= 3])

    # Calculate ASL and ASW
    asl = num_words / len(sentences)
    asw = num_syllables / num_words

    # Calculate the Flesch-Kincaid reading level
    reading_level = (0.39 * asl) + (11.8 * asw) - 15.59

    print(f'The Flesch-Kincaid reading level of the document is {reading_level}.')

    # Calculate the SMOG index
    smog_index = (1.043 * (30 * num_polysyllable_words / len(sentences))**0.5) + 3.1291
    print(f'The SMOG index of the document is {smog_index}.')

    # Define the rubric
    rubric = """
    Flesch-Kincaid Grade Level Interpretation:
    - Score around 1: Text is easily understandable by an average 1st grader.
    - Score around 6-7: Text is easily understandable by 6th to 7th graders.
    - Score around 12: Text is easily understandable by high school graduates.
    - Score above 12: Text is easily understandable by college-level students.
    """
    # Define the rubric for SMOG
    smog_rubric = """
    SMOG Index Interpretation:
    - Score around 1-5: Text is easily understandable by elementary school students.
    - Score around 6-8: Text is easily understandable by middle school students.
    - Score around 9-12: Text is easily understandable by high school students.
    - Score above 12: Text is easily understandable by college-level students.
    """
    # Write the results to a file
    with open('reading_level_results.txt', 'a') as f:
        f.write(f'\nDocument: {os.path.basename(file_path)}\n')
        f.write(f'The Flesch-Kincaid reading level of the document is {reading_level}.\n')
        f.write(rubric)
        f.write(f'\nThe SMOG index of the document is {smog_index}.\n')
        f.write(smog_rubric)

# Call the function with the file path and the starting text
evaluate_readability('Readability_Pharmacogenetics (PGx) AI Assistant - Responses for Patient.docx', 'AI Assistant:')
evaluate_readability('Readability_ChatGPT 3.5 PGx Responses - Responses for Patient.docx', 'ChatGPT 3.5:')
