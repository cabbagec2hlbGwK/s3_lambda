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
resource "aws_iam_policy" "s3_read_allow_POL" {
  name        = "s3_allow_read"
  description = "A poliocy which allows read access to s3"

  # Define your policy document here
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
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
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
resource "aws_iam_policy_attachment" "example_attachment" {
  name       = "policy1212332"
  policy_arn = aws_iam_policy.s3_read_allow_POL.arn
  roles      = [aws_iam_role.iam_for_lambda.name]
}
