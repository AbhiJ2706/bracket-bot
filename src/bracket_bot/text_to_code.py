import anthropic
from dotenv import load_dotenv
import os

def generate_robot_code(user_command: str) -> str:
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment variable
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    # Initialize client with API key
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = """
    You are an expert at controlling a two-motor drive robot. Your goal is to generate Python code that leverages the RobotController class to perform various movements and maneuvers.
    ### Template Setup:
    ```python
    from robot_motion import RobotController
    import math
    import random
    import time
    controller = RobotController()
    # Your robot control commands will go here
    # Make sure to call the methods as controller.method_name()
    # Make sure to add this template to your code
    controller.cleanup()
    ```
    ### Available Methods:
    - **drive_distance(distance_meters:float)**: Moves the robot forward/backward for the specified distance in meters.
    - **turn_degrees(degrees:float)**: Turns the robot by a specified degree offset.
    ### Instructions:
    - Use RobotController methods to command the robot.
    - The final output should be pure Python code using RobotController only.
    Now, **only output Python code** that satisfies these requirements and showcases various robot maneuvers. The output should be plain Python code using the RobotController class. It must not input any other text.
    """.strip()

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8096,
        messages=[
            {"role": "user", "content": prompt + user_command}
        ]
    )
    
    response = message.content[0].text
    
    # Clean up the code by removing markdown code blocks and empty lines
    cleaned_code = '\n'.join(
        line for line in response.split('\n')
        if not line.startswith('```') and line.strip()
    ).strip()

    
    return cleaned_code

def run_generated_code(code_string:str)->bool:
    """
    Executes the generated robot code in a safe manner.
    
    Args:
        code_string (str): The Python code to execute
    """
    try:
        exec(code_string)
        
        return True
    except Exception as e:
        print(f"Error executing robot code: {str(e)}")
        return False


