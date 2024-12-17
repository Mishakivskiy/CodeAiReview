from openai import OpenAI

async def analyze_code(files: list, assignment_description: str, level: str, openai_token: str):
    json_example = {
        'downsides': 'List[str] - downsides',
        'rating': f'Rating: x/5 (for {level} level)',
        'conclusion': 'str'
    }
    prompt = f"""
    Analyze the following files for a {level} developer's assignment "{assignment_description}, 
    like a professional developer": {files}, describe all the shortcomings, rate from 1 to 5 and write final conclusion,
    answer in json format: {json_example}, RETURN OLY JSON CODE!
    """
    client = OpenAI(
        api_key=openai_token,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-turbo",
    )
    return response.choices[0].message.content
