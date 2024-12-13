import base64
from openai import OpenAI
from dotenv import load_dotenv
import json
import argparse
import sys

load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
  
def get_class(image_path, model_name="gpt-4o-mini", image_res="low"):
    #0 is returned for nota
    #1 is returned for BAR
    #2 is returned for LINE
    #3 is returned for PIE
    client = OpenAI()
    base_64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Classify the image as one of the 4 classes: Bar graph, line chart, pie chart or None of the Above.",
                },
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/jpeg;base64,{base_64_image}",
                    "detail": image_res
                },
                },
            ],
            }
        ],
    )
    
    message = response.choices[0].message.content.lower()
    if "bar" in message:
        return 1
    elif "line" in message:
        return 2
    elif "pie" in message:
        return 3
    
    return 0

def summarize_chart(image_path, image_class, model_name="gpt-4o", image_res="high"):
    if image_class==1:
        gpt_prpt_str = "bar"
    elif image_class==2:
        gpt_prpt_str = "line"
    elif image_class==3:
        gpt_prpt_str = "pie"
    else:
        return
    
    client = OpenAI()
    base_64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"You are a data analyst tasked with describing the key information from a {gpt_prpt_str} chart. Provide a summary for the given graph which includes a detailed information about the features and datapoints.",
                },
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/jpeg;base64,{base_64_image}",
                    "detail": image_res
                },
                },
            ],
            }
        ],
    )

    return response.choices[0].message.content

def get_attributes_chart(image_path, image_class, model_name="gpt-4o", image_res="high"):
    if image_class==1:
        gpt_prpt_str = "bar"
    elif image_class==2:
        gpt_prpt_str = "line"
    elif image_class==3:
        gpt_prpt_str = "pie"
    else:
        return
    
    client = OpenAI()
    base_64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"Try to capture these attributes: legend, chart title, XY-axis titles, and XY-axis labels in a JSON format from the given {gpt_prpt_str} chart. Also try to capture any datapoints if possible.",
                },
                {
                "type": "image_url",
                "image_url": {
                    "url":  f"data:image/jpeg;base64,{base_64_image}",
                    "detail": image_res
                },
                },
            ],
            }
        ],
    )

    try:
        return json.loads(response.choices[0].message.content.strip('```json\n').strip('```'))
    except:
        pass
        
    return response.choices[0].message.content

def parse_args():
    parser = argparse.ArgumentParser(description="GPT chart analyser")
    parser.add_argument("--image_path", dest="image_path", help="test images", default="test", type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    image_class = get_class(args.image_path)
    if image_class==0:
        print("The image belongs to none of the mentioned classes: bar, pie and line charts.")
        sys.exit(0)
    elif image_class==1:
        print("The image is a bar graph\n")
    elif image_class==2:
        print("The image is a line chart\n")
    else:
        print("The image is a pie chart\n")

    summary = summarize_chart(args.image_path, image_class)
    print("Below is the summary of the chart in the provided image:")
    print(summary)

    outp_json = get_attributes_chart(args.image_path, image_class)
    print("\nBelow is the json of important attributes of the chart:")
    print(outp_json)
