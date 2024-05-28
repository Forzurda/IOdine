import discord
import re


def embed_success(desc):
    return discord.Embed(
            description=":ballot_box_with_check: " + desc,
            color=15879747
        )


def embed_failure(desc):
    return discord.Embed(
            description=":x: " + desc,
            color=15879747
        )


def divide_chunks(content, size):
    for i in range(0, len(content), size):
        yield content[i:i + size]