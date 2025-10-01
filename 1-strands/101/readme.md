# aws commands

0. Setup:

# virtual env 
source ~/venv/bin/activate

# test local setup
aws sts get-caller-identity  
aws iam get-user
  

1. Check models with access in region:
```
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[?contains(modelId, `anthropic`)].[modelId, modelName]' --output table
```
2. Run basic_1.py
3. Run basic_2.py
