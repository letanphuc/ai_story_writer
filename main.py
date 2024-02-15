from reviewer import review
from fixer import fixer
from story import story
from writer import write

from loguru import logger

language = "Vietnamese"
topic = "một câu chuyện cho thiếu nhi về loài thỏ bằng tiếng Việt, có các yếu tố gia đình, bạn bè, và quay về nhà"

if __name__ == '__main__':
    if not story.was_written():
        logger.info("Start writing")
        write(topic, language)
    for i in range(3):
        try:
            commend = review(story.as_str(), language)
            logger.info(f"Review round {i}: {commend}")
            fixer(story.last_review(), story.as_str(), language)
            logger.info(f"Finish round {i}")
        except Exception as e:
            logger.error(f'{e=}')
    print(story.as_str())
