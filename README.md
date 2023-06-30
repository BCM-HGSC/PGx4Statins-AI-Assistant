### About PGx-slco1b1-chatbot

The project described aims to explore the potential of GenAI, specifically GPT-4, in the field of genetic counseling and personalized care. The primary objective is to improve the accessibility and interpretation of genetic test results, with a specific focus on genetic testing for predicting responses to drug therapies.

By leveraging the capabilities of GenAI, the project seeks to enhance the process of genetic counseling, making it more efficient and effective for both patients and healthcare providers. This technology has the potential to assist in the interpretation of complex genetic data, providing valuable insights into the predicted response to drug therapies. This, in turn, can contribute to personalized care plans that are tailored to individual patients based on their genetic makeup.

In addition to improving accessibility and interpretation, the project also recognizes the importance of addressing the risks associated with the adoption of GenAI. Patient safety is a critical concern, and the study aims to evaluate and implement practical safeguards to mitigate these risks. By doing so, the project seeks to ensure that the integration of GenAI into clinical practice is responsible and safe for patients.

The overall goal of this project is to gain a comprehensive understanding of how GenAI can enhance personalized care in the field of clinical genetics. By utilizing this innovative technology, the project aims to reduce disparities in accessing genetic information, promote equitable access to personalized care, and ultimately improve patient outcomes.

### Getting Started with PGx-slco1b1-chatbot
#### Check out the project
```commandline
cd </path/to/project>
git clone https://github.com/BCM-HGSC/PGx-slco1b1-chatbot.git
```
#### Setup python environment

Since packages need python version >=3.7 and <3.10, we recommend creating python virtual environment with python 3.9. 

```
1. cd </path/to/project/>PGx-slco1b1-chatbot
2. python3.9 -m venv <virtual-environment-name>
3. source <virtual-environment-name>/bin/activate
4. pip install --upgrade pip
5. pip install -r requirements.txt
```

#### Run the project
Before running the application, something needs to be configured in the config.yaml file. You can specify the local vector chroma database settins and the path to the data file in the config.yaml file. We provide data files in data folder, which includes some csv and pdf files for demo. For the pdf file, the chunk size and overlap size and configurable in the config.yaml file. Since we can openai api to do question answering, you can replace the following line in the config.yaml file:
```
openai:
  api_key: sk-xxxx
```

with your account's secret key which is available on the [website](https://platform.openai.com/account/api-keys). But we recommand you set it as the OPENAI_API_KEY environment variable before running the application:
```
export OPENAI_API_KEY='sk-xxxx'
```

##### Insert the data into the vector database chroma
```
1. cd </path/to/project>/PGx-slco1b1-chatbot
2. python upsert.py -y config.yaml
```

##### Question and Answering
```
1. cd </path/to/project>/PGx-slco1b1-chatbot
2. python question_answering.py -y config.yaml
```

Enjoy it!