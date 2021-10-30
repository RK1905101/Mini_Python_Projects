import pyjokes
import click

"""
USAGE: 
    python command_line_pyjokes.py -l en -c chuck
        where 'en' is the language and 'chuck' is the category (both arguments are optional)
    python command_line_pyjokes.py --help 
        to get more information on usage.
"""


@click.command()
@click.option(
    "--language", "-l", default="en", help="Select the language of the joke among: 'en', 'de', 'es', 'gl' , 'eus'"
)
@click.option("--category", "-c", default="neutral", help="Select a category among: 'neutral', 'chuck', 'all'")
def joke(language, category):
    """Simple function that tells nerdy jokes according to chosen language & category."""
    print(
        pyjokes.get_joke(
            language=language,
            category=category
        )
    )


if __name__ == "__main__":
    joke()
