# Pulled from lab 08, follow this template for util/services!

def search_string(name: str, substring: str):
    return substring.strip().lower() in name.lower()


def title_for_sorting(title: str) -> str:
    # Only extracts alphabets for sorting (no digits and special characters)
    alphabet_list = [char.lower() for char in title if char.isalpha()]
    alphabets = ''.join(alphabet_list)

    # If there are alphabets in title, return it for sorting
    # The title should start with alphabets to be prioritized for sorting.
    if alphabets and title[0].isalpha():
        return alphabets

    return f'z{title}'


# Sort list of entities by title alphabetically,
# such as list of podcasts that have title attributes


def sort_entities_by_title(items: list) -> list:
    items.sort(key=lambda entity: title_for_sorting(entity.title))
    return items
