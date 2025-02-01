def summarize_text(client, text, num_sentences=6, model="gpt-4o-mini"):
    """
    Summarize the given text using GPT-4 API.
    """
    try:
        # Ensure text is a string
        if not isinstance(text, str):
            raise ValueError("Input must be a string")

        # Use OpenAI's new ChatCompletion API
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert summarizer."},
                {"role": "user", "content": f"Please summarize the following text in {num_sentences} sentences: {text}"}
            ],
            model=model
        )

        # Extract and return the summary
        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        raise Exception(f"Error summarizing text: {str(e)}")