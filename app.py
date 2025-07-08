import gradio as gr
import boto3
import os

# -----------------------------
# Code Generation Function (Region and Model ID from UI)
# -----------------------------
def generate_code(region, model_id, prompt):
    """
    Sends the user's prompt to the selected Bedrock model and returns the generated code.
    AWS region and model ID are provided by the user via the UI.
    Handles errors gracefully and provides user-friendly messages.
    """
    # Check for required UI inputs
    missing_vars = []
    if not region:
        missing_vars.append('AWS Region')
    if not model_id:
        missing_vars.append('Bedrock Model ID')
    if missing_vars:
        return f"Error: Missing required input(s): {', '.join(missing_vars)}"

    if not prompt or not prompt.strip():
        return "Please enter a valid prompt."

    # Initialize the Bedrock client with region from UI (uses IAM Role if available)
    try:
        client = boto3.client(
            'bedrock-runtime',
            region_name=region
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
            modelId=model_id,
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
# Gradio UI Setup (Region, Model ID, Prompt)
# -----------------------------
def main():
    """
    Launches the Gradio app for the coding assistant.
    The user provides AWS region, Bedrock model ID, and the prompt via the UI.
    """
    description = """
    # My Coding Assistant\n\n
    Enter the AWS region, Bedrock model ID, and your coding prompt. The assistant will generate code using your selected Bedrock model.\n\n
    (AWS credentials are securely provided by the environment or IAM Role.)
    """
    iface = gr.Interface(
        fn=generate_code,
        inputs=[
            gr.Textbox(lines=1, label="AWS Region"),
            gr.Textbox(lines=1, label="Bedrock Model ID"),
            gr.Textbox(lines=4, label="Enter your coding prompt")
        ],
        outputs=gr.Code(label="Generated Code"),
        title="My Coding Assistant",
        description=description,
        allow_flagging='never',
        theme="default"
    )
    iface.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
