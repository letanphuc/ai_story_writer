import os.path

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import re
import shutil
from loguru import logger
from story import story, Chapter

load_dotenv()

version = 0


@tool
def save_chapter(chapter: int, title: str, content: str):
    """Save content into chapter at number with title"""
    logger.info(f"Saving chapter {chapter} with title {title}")
    story.add_chapter(chapter, title, content)


writer_prompt = ChatPromptTemplate.from_template("""
write a short story in {lang} of following topic:
{topic}

Story shall be written in less than 8 chapters and be writen chapter by chapter.
A chapter shall be about 10-20 sentences.
""")


def write(t, l):
    tools = [save_chapter]
    prompt = hub.pull("hwchase17/structured-chat-agent")
    model = ChatOpenAI()
    agent = create_structured_chat_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor.invoke({'input': writer_prompt.format(topic=t, lang=l)})


if __name__ == '__main__':
    topic = "một câu chuyện cho thiếu nhi về loài thỏ bằng tiếng Việt, có các yếu tố gia đình, bạn bè, và quay về nhà"
    lang = 'Vietnamese'
    write(topic, lang)
