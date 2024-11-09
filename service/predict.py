from nltk.corpus import words
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from string import punctuation
from transformers import BertTokenizer, BertForMaskedLM
import errno
import nltk
import os
import torch


def init_models(mask='<blank>'):
    global model_word
    global model_sentiment
    global tokenizer
    global token
    global token_id
    global acceptable_words

    # Step 1: Change Hugging Face and NLTK cache directory
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    nltk_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
    nltk.data.path.append(nltk_dir)

    # Create Hugging Face cache directory if not exists
    try:
        os.makedirs(cache_dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Directory already exists
            pass
        else:
            raise

    # Create NLTK cache directory if not exists
    try:
        os.makedirs(nltk_dir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            # Directory already exists
            pass
        else:
            raise


    # Step 2: Choose a pre-trained BERT model architecture and an NLTK lexicon
    pretrained_bert_model = 'bert-base-uncased'
    nltk_lexicon = 'vader_lexicon'
    nltk_words = 'words'


    # Step 3: Load a pre-trained Bert model for predicting a masked word in a sentence
    try:
        model_word = BertForMaskedLM.from_pretrained(pretrained_model_name_or_path=pretrained_bert_model, cache_dir=cache_dir, local_files_only=True)
    except OSError:
        print(f"Model not found locally. Downloading {pretrained_bert_model}...")
        model_word = BertForMaskedLM.from_pretrained(pretrained_model_name_or_path=pretrained_bert_model, cache_dir=cache_dir)
        model_word.eval()


    # Step 4: Load a pre-trained model tokenizer (vocabulary)
    try:
        tokenizer = BertTokenizer.from_pretrained(pretrained_model_name_or_path=pretrained_bert_model, cache_dir=cache_dir, local_files_only=True)
    except OSError:
        print(f"Tokenizer not found locally. Downloading {pretrained_bert_model}...")
        tokenizer = BertTokenizer.from_pretrained(pretrained_model_name_or_path=pretrained_bert_model, cache_dir=cache_dir)


    # Step 5: Download NLTK resources
    nltk.download(nltk_lexicon, download_dir=nltk_dir)
    nltk.download(nltk_words, download_dir=nltk_dir)


    # Step 6: Set <blank> as the search token and add it to the tokenizer as a new special token
    token = mask
    additional_special_tokens_dict = {'additional_special_tokens': [token,]}
    tokenizer.add_special_tokens(additional_special_tokens_dict)
    token_id = tokenizer.encode(text=token, return_tensors='pt')[0,1].item()


    # Step 7: Update BERT models based on tokenizer changes
    model_word.resize_token_embeddings(len(tokenizer))


    # Step 8: Load an NLTK model for the sentiment analysis
    model_sentiment = SentimentIntensityAnalyzer()


    # Step 9: Set the set of acceptable words as predictions
    acceptable_words = set(words.words())


def validate_text(text: str):
    # Igore text which does not contain the <blank> token
    if token not in text:
        return False

    return True


def predict_words(text: str, k: int = 20):
    # Convert the text to lowercase
    text_lowercase = text.lower()

    # Get token IDs of the input sentence
    input_ids = tokenizer.encode(text=text_lowercase, return_tensors='pt')

    # Get position of the <blank> token
    mask_token_index = torch.where(input_ids == token_id)[1]

    # Predict all tokens
    with torch.no_grad():
        outputs = model_word(input_ids)
        predictions = outputs[0]

    # Get top K predicted words
    top_k_predicted_indices = torch.topk(predictions[0, mask_token_index].flatten(), k).indices

    # Ensure predicted words are English words
    return_words = []

    for idx in top_k_predicted_indices.tolist():
        word = tokenizer.decode([idx])
        if word in acceptable_words:
            return_words.append(word)

    return return_words


def remove_negative_sentiment(text: str, words: list):
    acceptable_words = []

    for word in words:
        final_text = text.replace(token, word)
        polarity_scores = model_sentiment.polarity_scores(final_text)

        # Ignore words with negative polarity and words whose neutral polarity is higher than their positive polarity
        if polarity_scores['neg'] == 0 and polarity_scores['pos'] > polarity_scores['neu']:
            acceptable_words.append(word)

    return acceptable_words


model_word = None
model_sentiment = None
tokenizer = None
token = None
token_id = None
acceptable_words = None
