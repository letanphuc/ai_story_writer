from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from writer import save_chapter
from story import story

load_dotenv()

fixer_prompt = ChatPromptTemplate.from_template("""
Rewrite a chapter of story in {lang} with given review.
Chapter index is given in review. 
RESPOND TO ME FULL OF UPDATED STORY ONLY, NO MORE ADDITIONAL TEXT

Review:
-------
{review}

Story:
------
{story}
""")


def fixer(r, s, l="Vietnamese"):
    tools = [save_chapter]

    prompt = hub.pull("hwchase17/structured-chat-agent")
    model = ChatOpenAI()

    agent = create_structured_chat_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor.invoke({'input': fixer_prompt.format(review=r, story=s, lang=l)})


if __name__ == '__main__':
    review_comment = story.last_review()
    story_content = story.as_str()

    fixer(review_comment, story_content)
    story.save()
