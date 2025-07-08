import gradio as gr
import boto3
import os

# -----------------------------
# Code Generation Function (Updated)
# -----------------------------
def generate_code(access_key, secret_key, region, model_id, prompt):
    """
    Sends the user's prompt to CodeLlama via Amazon Bedrock and returns the generated code.
    Accepts AWS credentials and model details from the user via the UI.
    Handles errors gracefully and provides user-friendly messages.
    """
    if not prompt or not prompt.strip():
        return "Please enter a valid prompt."
    if not access_key or not secret_key or not region or not model_id:
        return "Please provide all required AWS credentials and model details."

    # Initialize the Bedrock client with user-provided credentials
    try:
        client = boto3.client(
            'bedrock-runtime',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
    except Exception as e:
        return f"Failed to initialize Bedrock client: {e}"

    # Prepare the request payload for CodeLlama
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
# Gradio UI Setup (Updated)
# -----------------------------
def main():
    """
    Launches the Gradio app for the coding assistant.
    Now accepts AWS credentials and model details from the user.
    """
    description = """
    # CodeLlama Coding Assistant 🦙\n
    Enter your AWS credentials, region, and Bedrock model ID.\n
    Then, enter a prompt describing the code you want. The assistant will generate code using CodeLlama via Amazon Bedrock.
    """
    iface = gr.Interface(
        fn=generate_code,
        inputs=[
            gr.Textbox(lines=1, label="AWS Access Key ID"),
            gr.Textbox(lines=1, label="AWS Secret Access Key", type="password"),
            gr.Textbox(lines=1, label="AWS Region", value="us-east-1"),
            gr.Textbox(lines=1, label="Bedrock Model ID", value="codellama"),
            gr.Textbox(lines=4, label="Enter your coding prompt")
        ],
        outputs=gr.Code(label="Generated Code"),
        title="CodeLlama Coding Assistant",
        description=description,
        allow_flagging='never',
        theme="default"
    )
    iface.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
