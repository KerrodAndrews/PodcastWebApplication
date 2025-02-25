# general imports:
import os
from flask import Flask, session
from dotenv import load_dotenv

# blueprint imports:
#from podcast.blueprints import playlists

# adapters imports:
import podcast.adapters.abstract_repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.orm import mapper_registry, map_model_to_tables

# sqlalchemy imports:
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from podcast.domainmodel.model import User


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Oceans Of Sound"
    app.secret_key = "Oceans Of Sound"
    load_dotenv()
    repository_type = os.getenv('REPOSITORY', 'memory')

    if repository_type == 'database':
        database_uri = 'sqlite:///podcasts.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

        # Create a database engine and connect it to the specified database
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=False)

        # Create the database session factory using session maker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        # Create the SQLAlchemy DatabaseRepository instance for a sqlite3-based repository.
        repo.repo_instance = SqlAlchemyRepository(session_factory)

        if len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            mapper_registry.metadata.create_all(database_engine)

            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            map_model_to_tables()

            repo.repo_instance.populate()
            print("REPOPULATING DATABASE... FINISHED")

        else:
            map_model_to_tables()
    else:
        from podcast.adapters.memory_repository import MemoryRepository
        repo.repo_instance = MemoryRepository()
        repo.repo_instance.populate()

    # Builds pages using blueprints
    with app.app_context():
        # Register blueprints.
        from .blueprints import authentication, catalogue, home, podcast_description, search_query, playlists
        app.register_blueprint(authentication.authentication_blueprint)
        app.register_blueprint(catalogue.catalogue_blueprint)
        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(podcast_description.podcast_description_blueprint)
        app.register_blueprint(search_query.catalogue_blueprint)
        app.register_blueprint(playlists.playlists_blueprint)

    @app.context_processor
    def inject_user():
        username = session.get('username', '')
        return {'username': username}

    return app
