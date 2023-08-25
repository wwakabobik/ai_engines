""" This module contains implementation for Custom Translator """
# -*- coding: utf-8 -*-

from deep_translator import GoogleTranslator


class CustomTranslator(GoogleTranslator):
    """
    This class implements wrapper for GoogleTranslator
    """
    def __init__(self, source, target, **kwargs):
        """
        General init.

        :param source: source language (string).
        :param target: target language (string)
        :param kwargs: Custom arguments, optional.
        """
        super().__init__(source, target, **kwargs)
        self.___source = source
        self.___target = target

    @property
    def source(self):
        """
        Getter for source.

        :return: The source.
        """
        return self.___source

    @source.setter
    def source(self, value):
        """
        Setter for source.

        :param value: The source.
        """
        self.___source = value

    @property
    def target(self):
        """
        Getter for source.

        :return: The source.
        """
        return self.___target

    @target.setter
    def target(self, value):
        """
        Setter for target.

        :param value: The source.
        """
        self.___target = value

    def translate(self, text: str, **kwargs) -> str:
        """

        :param text: Text (string) to translate.
        :param kwargs: Custom arguments, optional.
        :return: string, translated text.
        """
        return super().translate(text)
