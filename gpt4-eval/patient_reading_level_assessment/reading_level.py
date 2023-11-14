import docx
import nltk
import pyphen

# Load the document
doc = docx.Document('Patient_Questions_AIAssistantResponses.docx')

# Extract all text that starts with the prefix 'Answer'
text = ' '.join([para.text[len('Answer: '):] for para in doc.paragraphs if para.text.startswith('Answer: ')])

# Split the text into sentences
sentences = nltk.sent_tokenize(text)

# Initialize counters
num_words = 0
num_syllables = 0

# Create a Pyphen object for counting syllables
dic = pyphen.Pyphen(lang='en')

# For each sentence, split it into words and count the number of words and syllables
for sentence in sentences:
    words = nltk.word_tokenize(sentence)
    num_words += len(words)
    num_syllables += sum([len(dic.inserted(word).split('-')) for word in words])

# Calculate ASL and ASW
asl = num_words / len(sentences)
asw = num_syllables / num_words

# Calculate the Flesch-Kincaid reading level
reading_level = (0.39 * asl) + (11.8 * asw) - 15.59

print(f'The Flesch-Kincaid reading level of the document is {reading_level}.')
