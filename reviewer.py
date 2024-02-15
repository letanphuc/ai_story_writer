from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from story import story

load_dotenv()

reviewer_prompt = ChatPromptTemplate.from_template("""
Review following story, give exactly 1 point which must be improved, make it short and directly
Review in {lang}

Story:
-----
{story}

RESPOND TO ME IN FOLLOWING FORMAT, NO MORE ADDITIONAL TEXT:
----------------------------------------------------------
Weak Point: ...
Effected chapters: ... \\ a list of chapter numbers, example: 1, 3, 6
Suggestion: ...

With x is index of review chapter

""")

review_count = 0


def review(s, l='Vietnamese'):
    global review_count
    model = ChatOpenAI()
    reviewer = reviewer_prompt | model | StrOutputParser()
    review_comment = reviewer.invoke({'story': s, 'lang': l})
    story.add_review(review_comment)
    return review_comment


if __name__ == '__main__':
    comment = review(story.as_str(), "Vietnamese")
    print(comment)
