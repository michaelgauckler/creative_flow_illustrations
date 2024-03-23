# Michael Gauckler, 2024, released under Attribution-ShareAlike 4.0 International (https://creativecommons.org/licenses/by-sa/4.0/)

import requests
import datetime
import time
import openai
import os

# Constants
nofimages = 10  # Number of images to generate
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    """
    Summarizes the given text into the most relevant 5 words joined with dashes,
    using the OpenAI ChatGPT model via the chat completions endpoint.
    
    :param text: The text to be summarized.
    :return: A string of the most relevant 5 words joined with dashes.
    """
    try:
        # Adjust the call to use the chat completions endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Adjust based on the available ChatGPT model
            messages=[{"role": "system", "content": "Summarize the following text into the most relevant 5 words:"},
                      {"role": "user", "content": text}]
        )
        
        # Extracting the summary from the response
        summary = response['choices'][0]['message']['content']
        # Process the summary to get the desired format
        summary_words = summary.split()
        if len(summary_words) > 5:
            summary = '-'.join(summary_words[:5])
        else:
            summary = '-'.join(summary_words)
        
        return summary.strip().replace(".", "").replace(",", "")

    except Exception as e:
        print(f"Encountered an error while summarizing: {e}")
        return None

def generate_filename(summary):
    """Generates a filename using the current date, time, and a summary."""
    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    return f"{date_time}-{summary}"

def read_file(file_path):
    """Reads and returns the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_prompt(filename, prompt):
    """Saves the prompt to a file."""
    with open(f"{filename}.txt", 'w', encoding='utf-8') as file:
        file.write(prompt)


def download_image(image_url, save_path):
    """Downloads an image from a URL and saves it to a file."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.

        with open(save_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else {err}")

def call_api_and_save_images(prompt, filename):
    for i in range(nofimages):
        try:
            # Hypothetical function call, adjust based on actual API capabilities
            response = openai.Image.create(
                prompt=prompt,
                n=1,  # Generate one image at a time in this loop
                model="dall-e-3",  # Specify the model to use DALL·E 3
            )
            #print (f"response: {response}")
            img_data = response['data'][0]['url']  # Assuming the response contains image URLs
            img_filename = f"{filename}-{i+1:02d}.png"

            # Assuming we need to download the image from the URL, which requires additional code not shown here
            download_image(img_data, img_filename)

        except Exception as e:  # Adjusted to catch a more general exception
            print(f"Encountered an error: {e}")
            time.sleep(120)  # Wait for 2 minutes before retrying

def main():
    # Read the input and auxiliary texts
    input_text = read_file("input.txt")
    pre_prompt = read_file("pre-prompt.txt")
    post_prompt = read_file("post-prompt.txt")

    # Summarize and generate filename
    summary = summarize_text(input_text)
    filename = generate_filename(summary)

    # Assemble the full prompt
    full_prompt = f"{pre_prompt}\n{input_text}\n{post_prompt}"

    # Save the prompt to a file
    save_prompt(filename, full_prompt)

    # Output the complete prompt, the summary, and the filename to the console
    print("Complete Prompt:")
    print(full_prompt)
    print("\nSummary:")
    print(summary)
    print("\nFilename:")
    print(filename)

    # Call API and save images
    call_api_and_save_images(full_prompt, filename)

if __name__ == "__main__":
    main()
