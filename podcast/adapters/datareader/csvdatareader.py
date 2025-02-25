import os
import csv
from podcast.domainmodel.model import *

"""
The CSVDataReader class has been updated to no longer access domain model objects, as referenced in our A1 feedback.
It now simply stores the raw data in a rudimentary dictionary, ready to be processed and stored as actual Podcast/Author
objects by the Memory Repository. It also accesses the CSV files with the appropriate encoding scheme.
"""


class CSVDataReader:
    def __init__(self):
        self.__podcast_data = []
        self.__episode_data = []
        self.__categories_data = set()
        self.__authors_data = set()

        self.podcasts_filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'podcasts.csv')  #moves filepath
        # up one directory, then navigates to the podcasts.csv file.
        self.episodes_filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'episodes.csv')  #does the same
        # but for our 'episodes' dataset.

        self.load_podcast_data()
        self.load_episode_data()

    def load_podcast_data(self):
        with open(self.podcasts_filepath, "r", encoding='utf-8-sig') as podcast_file:
            podcasts_rows = csv.DictReader(podcast_file)
            author_count = 1
            category_count = 1
            for row in podcasts_rows:
                try:
                    podcast_id = int(row["id"])
                    podcast_title = row["title"]
                    podcast = Podcast(podcast_id, podcast_title)

                    author_name = row["author"]
                    if author_name == '':
                        author_name = 'No Author Listed.'
                    author = Author(author_count, author_name)
                    if author.name not in [x.name for x in self.__authors_data]:
                        self.__authors_data.add(author)
                        author_count += 1
                    else:
                        author = next(existing_author for existing_author in self.__authors_data if existing_author.name == author.name)

                    podcast.author = author

                    podcast.description = row["description"]
                    podcast.image = row["image"]
                    podcast.language = row["language"]
                    if podcast.language == '':
                        podcast.language = "No Language information available."
                    if row["website"] == '':
                        podcast.website = "No website listed."
                    else:
                        podcast.website = row["website"]
                    podcast.itunes_id = row["itunes_id"]

                    # Handle categories similarly to avoid duplicates
                    category_names = row["categories"].split("|")
                    for category_name in category_names:
                        category = Category(category_count, category_name.strip())
                        if category.name not in [x.name for x in self.__categories_data]:
                            self.__categories_data.add(category)
                            category_count += 1
                        else:
                            # Retrieve the existing category instance from the set
                            category = next(existing_category for existing_category in self.__categories_data if
                                            existing_category.name == category.name)
                        podcast.add_category(category)

                    # Add the podcast to the podcast data list
                    self.__podcast_data.append(podcast)

                except ValueError as e:
                    print(e)
                    pass  # Skip row due to invalid data
                except KeyError as e:
                    print(e)
                    pass  # Skip row due to missing key


    def load_episode_data(self):
        podcast_lookup = {p.id: p for p in self.__podcast_data}

        with open(self.episodes_filepath, "r", encoding='utf-8-sig') as episode_file:
            # id,podcast_id,title,audio,audio_length,description,pub_date
            episodes_rows = csv.DictReader(episode_file)

            # Iterate through all rows in the CSV
            for row in episodes_rows:
                episode_id = int(row["id"])
                podcast_id = int(row["podcast_id"])  # Podcast ID for the current episode

                # Efficient lookup for the podcast using the dictionary
                podcast = podcast_lookup.get(podcast_id)

                # Ensure the podcast was found
                if podcast is not None:
                    title = row["title"]
                    audio = row["audio"]
                    audio_length = int(row["audio_length"])
                    description = row["description"]
                    publish_datetime = datetime.strptime(row["pub_date"] + ":00", '%Y-%m-%d %H:%M:%S%z')  # the '+":00"'
                    #  avoids a parsing error when converting to a datetime object.
                    publish_date, publish_time = publish_datetime.date(), publish_datetime.time()

                    # Create episode object
                    episode = Episode(episode_id, podcast, title, audio, audio_length, description, publish_date, publish_time)

                    # Add the episode to the podcast and repository
                    podcast.add_episode(episode)
                    self.__episode_data.append(episode)

    def get_podcasts(self):
        return self.__podcast_data

    def get_episodes(self):
        return self.__episode_data

    def get_categories(self):
        return self.__categories_data

    def get_authors(self):
        return self.__authors_data
