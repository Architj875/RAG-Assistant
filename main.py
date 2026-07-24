from app.config.settings import settings
from app.utils.logger import logger


def main():
    print("Project Started")

    print(settings.MODEL_NAME)

    print(settings.CHUNK_SIZE)

    logger.info("Application Started")


if __name__ == "__main__":
    main()