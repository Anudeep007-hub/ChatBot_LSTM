
## Start the project by creating a virtual environment with command "python/python3 -m venv vir", then activate it. 

--> Starting front-end part
    * navigate to "cd ChatBot" 
    * Download the nodemodules with the command "npm install" 
    * Then start the project by entering "npm start" 
    * You can see a chatbot loaded on your browser, don't use it unless you run the backend part of it. 

--> Starting the backend server
    * navigate to "cd backend". 
    * Install the required packages using the command "pip/pip3 install -r requirements.txt". (Preferred to install in inside a virtual environmet, to overcome the bugs of overriding) 
    * Start the server with command "python/python3 test.py".

Use our techbot after setting up the front-end and backend running successfully.






### Project inforamtion -- Group number - 11 


### Group objective - Chatbot for Customer support



#### Group Details: 

1. Anudeep Tippabathuni - S20220010226 
2. Suguru Sai Kiran - S20220010212 
3. Tharun Kumar L - S20220010123 
4. Koushik Pula - S20220010156 


### Methodology

We all four started off with collecting dataset manually from websites like, "stack overflow", "linus tech tips" and "microsoft support". It's stored in "corpus" folder with structure ,


""""" 
{
      "tag": "wifi_troubleshooting",
      "patterns": [
        "Why can't I connect to Wi-Fi?",
        "How do I fix Wi-Fi connection issues?",
        "My Wi-Fi is not working",
        "Why is my Wi-Fi connection unstable?",
        "How do I reconnect to Wi-Fi after losing connection?"
      ],
      "response": [
        "Make sure Wi-Fi is turned on. Go to Settings > Network & Internet > Wi-Fi, then ensure it's enabled. Restart your modem and router if needed.",
        "Try restarting your router and device. If that doesn't work, update the network adapter driver through Device Manager.",
        "Run the Network Troubleshooter by going to Start > Settings > Network & Internet > Status, and select Network Troubleshooter."
      ],
      "source": "Microsoft Support (https://support.microsoft.com/en-us/help/10741/windows-fix-network-connection-issues)"
    },
"""""  

## Steps of our work :- 


### 1. **Data Loading**:
- The data is loaded from the file `data_mid_2.json`. This file contains multiple intents, each of which has **patterns** (example user inputs) and corresponding **tags** (categories or labels of the inputs). These tags are the target labels for our model.
- We also load the intents from the JSON file and start processing the data to prepare it for the model.

### 2. **Text Preprocessing**:
- **Tokenizing Sentences**: 
  - Each pattern (user query) is tokenized into individual words using the `nltk` tokenizer. 
  - These tokenized words are further processed by **lemmatizing**, which converts words to their base form (e.g., "running" becomes "run").
- **Word Collection**:
  - The lemmatized words are collected into a list called `words`, and the intent tags are stored in `classes`. These will be used later for building the model.
  - All the words (excluding special characters) are sorted and stored in a `words.pkl` file for future use.
  - Similarly, the unique intent classes are stored and saved in `classes.pkl`.

### 3. **Training Data Preparation**:
- **Bag of Words**:
  - A "Bag of Words" is generated for each pattern, where a list is created for each sentence, representing the presence (1) or absence (0) of each word in the `words` list.
  - For each sentence, we also create an **output row**, where each row represents the target tag (intent) for that sentence. For instance, if the intent for a sentence is "greeting", the corresponding index for "greeting" in the output array is set to 1, while others remain 0.
- **Shuffling and Splitting**:
  - The dataset is shuffled to ensure randomness in the training process.
  - The training data is then divided into features (`train_x`) and labels (`train_y`). The features contain the bag-of-words representation of the sentences, while the labels correspond to the intents (tags).

### 4. **Loading Additional Data for Model**:
- **Reusing Data**:
  - Another dataset (from `corpus/data_mid_2.json`) is used to further tokenize the sentences. The labels (tags) are encoded using `LabelEncoder`, which converts text labels into numerical values.
  - **Tokenizer** is applied to convert text data into sequences of numbers (representing words). These sequences are then **padded** to ensure they all have the same length (i.e., they are uniformly shaped for input into the model).

### 5. **Train-Test Split**:
- The padded sequences are split into two sets: **training data** (80%) and **validation data** (20%). This ensures that the model can be evaluated on unseen data while training.

### 6. **Model Architecture**:
- The architecture consists of:
  - **Embedding Layer**: The words are mapped into dense vectors of fixed size (in this case, each word is represented as a vector of size 10).
  - **LSTM Layers**: Two Long Short-Term Memory (LSTM) layers are added to the model. These layers are used to process sequential data and capture relationships between words.
    - The first LSTM layer outputs the entire sequence of hidden states.
    - The second LSTM layer outputs only the final hidden state.
  - **Dropout Layers**: Dropout layers help to prevent overfitting by randomly dropping some neurons during training.
  - **Dense Layers**: Two dense (fully connected) layers are used to process the output from the LSTM and classify the input into one of the intents.
  - **Softmax Activation**: The final layer uses a softmax activation function to predict the probability of each intent class.

### 7. **Model Compilation**:
- The model is compiled using the **Adam optimizer** with a learning rate of `0.002`. The loss function used is **sparse categorical cross-entropy**, suitable for multi-class classification problems.
- The model tracks accuracy as a metric during training.

### 8. **Model Training**:
- The model is trained for 200 epochs using a batch size of 4. During each epoch, the model learns from the training data and evaluates its performance on the validation data after each epoch.

### 9. **Model Evaluation**:
- After training, the model is evaluated on the validation set to compute **validation loss** and **validation accuracy**.
- These metrics indicate how well the model performs on unseen data (validation data) after the training process.

### 10. **Model and Tokenizer Saving**:
- Once the model is trained, it is saved as a file (`chatbot_model_v1.keras`) for later use.
- The **Tokenizer** and **LabelEncoder** objects are also saved as `.pkl` files. These are required during inference to preprocess new input data (converting text into sequences).
- The maximum length of input sequences (`max_len`) is stored in a separate file (`model_metadata.json`), which is useful for padding future inputs correctly.
