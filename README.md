# S3 lambda

# Terraform Project Documentation

This documentation provides an overview and setup instructions for a Terraform project that creates an S3 bucket, a Lambda function, and an S3 notification to trigger the Lambda function.

## Prerequisites

Before you begin, ensure you have the following prerequisites:

- [Terraform](https://www.terraform.io/downloads.html) installed on your local machine.
- Appropriate AWS credentials and IAM permissions to create and manage resources.

## **Deployment**

1. Clone this repository to your local machine.
2. Initialize Terraform in the project directory:
    
    ```bash
    bashCopy code
    terraform init
    
    ```
    
3. Review and customize the **`variables.tf`** file if necessary.
4. Deploy the resources using Terraform:
    
    ```bash
    bashCopy code
    terraform apply
    
    ```
    
5. After deployment, Terraform will output the S3 bucket name and Lambda function name. You can access them using:
    
    ```bash
    bashCopy code
    terraform output s3_bucket_name
    terraform output lambda_function_name
    
    ```
    

## **Clean-Up**

To destroy the created resources and clean up:

```bash
bashCopy code
terraform destroy

```

## **Conclusion**

This Terraform project creates an S3 bucket, a Lambda function, and an S3 notification to trigger the Lambda function. You can further customize this configuration to suit your specific needs.