from googletrans import Translator


translator = Translator()


if __name__ == "__main__":
    text = translator.translate("В рот енот!")
    print(text.text)
