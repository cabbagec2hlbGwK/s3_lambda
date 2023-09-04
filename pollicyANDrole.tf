data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}
resource "aws_iam_policy" "lambda_POL" {
  name        = "s3_allow_read"
  description = "A poliocy which allows read access to s3"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject",
          "s3:DeleteObject",
        ],
        Effect   = "Allow",
        Resource = [format("%s/*", aws_s3_bucket.bucket1.arn), aws_s3_bucket.bucket1.arn],
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = "*",
      },
      {
        Action = [
          "quicksight:CreateDataSource",
          "quicksight:DescribeDataSource",
          "quicksight:UpdateDataSource",
          "quicksight:DeleteDataSource",
          "quicksight:UpdateDataSourcePermissions",
          "quicksight:QueryDataSource",
          "quicksight:GenerateDataSet"
        ],
        Effect   = "Allow",
        Resource = "*",
      },
    ],
  })
}


resource "aws_iam_role" "iam_for_lambda" {
  name               = "iamforlambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}
resource "aws_iam_policy_attachment" "lambda_attachment" {
  name       = "policy1212332"
  policy_arn = aws_iam_policy.lambda_POL.arn
  roles      = [aws_iam_role.iam_for_lambda.name]
}

resource "aws_iam_policy" "quick_user_POL" {
  name        = "policy-for-quick-sight"
  description = "A poliocy which allows read access to s3"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ],
        Effect   = "Allow",
        Resource = [format("%s/*", aws_s3_bucket.bucket1.arn), aws_s3_bucket.bucket1.arn],
      },
    ],
    }
  )
}

data "aws_iam_role" "quicksight_role" {
  name = "aws-quicksight-service-role-v0"
}

resource "aws_iam_policy_attachment" "attach_quicksite_s3" {
  name       = "pol1212"
  policy_arn = aws_iam_policy.quick_user_POL.arn
  roles      = [data.aws_iam_role.quicksight_role.name]

}
