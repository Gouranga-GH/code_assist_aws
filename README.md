# My Coding Assistant

A web-based coding assistant that generates code using any model available via Amazon Bedrock.

## Features
- Enter your AWS credentials, region, and Bedrock model ID via the UI.
- Enter a coding prompt and receive generated code from your selected Bedrock model.
- No hardcoded model references—works with any Bedrock-supported model.

## Getting Started

### Prerequisites
- Python 3.8+
- AWS account with access to Amazon Bedrock and the desired model
- AWS credentials (Access Key ID and Secret Access Key) with Bedrock permissions

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App Locally
```bash
python app.py
```
- Open your browser to `http://localhost:7860`
- Enter your AWS credentials, region, Bedrock model ID, and your coding prompt in the UI.

### Required Information
| Field                   | Where to Get / How to Find                                      |
|-------------------------|-----------------------------------------------------------------|
| AWS Access Key ID       | AWS Console → IAM → Users → Security credentials                |
| AWS Secret Access Key   | AWS Console → IAM → Users → Security credentials                |
| AWS Region              | AWS Console (top right) or AWS Bedrock documentation            |
| Bedrock Model ID        | AWS Console → Amazon Bedrock → Model details/documentation      |
| Coding Prompt           | Enter in the UI                                                 |

## CI/CD Pipeline
- GitHub Actions workflow is set up in `.github/workflows/python-app.yml`.
- On every push or pull request to `main`, the workflow:
  - Checks out the code
  - Sets up Python
  - Installs dependencies
  - Checks for syntax errors

## Deployment
- The app is designed for easy deployment to AWS EC2 or any server that supports Python and Gradio.
- For EC2 deployment, follow the steps in the deployment section of this documentation (to be added).

## License
MIT 