import gradio as gr
import boto3
import os

# -----------------------------
# Configuration: Read from Environment Variables
# -----------------------------
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID')

# -----------------------------
# Code Generation Function (Environment-based config)
# -----------------------------
def generate_code(prompt):
    """
    Sends the user's prompt to the selected Bedrock model and returns the generated code.
    AWS credentials and model details are read from environment variables for security.
    Handles errors gracefully and provides user-friendly messages.
    """
    # Check for required environment variables
    missing_vars = []
    if not AWS_ACCESS_KEY_ID:
        missing_vars.append('AWS_ACCESS_KEY_ID')
    if not AWS_SECRET_ACCESS_KEY:
        missing_vars.append('AWS_SECRET_ACCESS_KEY')
    if not AWS_REGION:
        missing_vars.append('AWS_REGION')
    if not BEDROCK_MODEL_ID:
        missing_vars.append('BEDROCK_MODEL_ID')
    if missing_vars:
        return f"Error: Missing required environment variables: {', '.join(missing_vars)}"

    if not prompt or not prompt.strip():
        return "Please enter a valid prompt."

    # Initialize the Bedrock client with environment credentials
    try:
        client = boto3.client(
            'bedrock-runtime',
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
    except Exception as e:
        return f"Failed to initialize Bedrock client: {e}"

    # Prepare the request payload for the selected model
    body = {
        "prompt": prompt,
        "max_gen_len": 512,  # Adjust as needed
        "temperature": 0.2,  # Lower = more deterministic
        "top_p": 0.95
    }

    try:
        response = client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=bytes(str(body), 'utf-8'),
            accept='application/json',
            contentType='application/json'
        )
        # Parse the response
        result = response['body'].read().decode('utf-8')
        # The response format may vary; adjust parsing as needed
        # For demonstration, we assume the generated code is in 'generation' key
        import json
        result_json = json.loads(result)
        generated_code = result_json.get('generation', 'No code generated.')
        return generated_code
    except Exception as e:
        return f"Error generating code: {e}"

# -----------------------------
# Gradio UI Setup (Prompt Only)
# -----------------------------
def main():
    """
    Launches the Gradio app for the coding assistant.
    Only the prompt is entered by the user; all other config is from environment variables.
    """
    description = """
    # My Coding Assistant\n\n
    Enter a prompt describing the code you want. The assistant will generate code using your selected Bedrock model.\n\n
    (AWS credentials, region, and model ID are securely read from environment variables.)
    """
    iface = gr.Interface(
        fn=generate_code,
        inputs=gr.Textbox(lines=4, label="Enter your coding prompt"),
        outputs=gr.Code(label="Generated Code"),
        title="My Coding Assistant",
        description=description,
        allow_flagging='never',
        theme="default"
    )
    iface.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
