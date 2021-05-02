def get_sentence_text(sentence):
    """
    :param sentence: UD sentence
    :return: text version of the UD sentence
    """
    text = ""
    contractions = ["'s", "'t", "'m", "'ll", "'ve", "'re", "'d"]

    for token in sentence:
        if not token.is_multiword() and token.form:
            if text != "" and token.form in contractions:
                text = text.rstrip()
            text += token.form + " "
    print(text[:-1])
    return text[:-1]
