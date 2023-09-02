provider "aws" {
  region = var.region
}

resource "aws_lambda_function" "data_check" {
  filename      = "code.zip"
  function_name = "data_check"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "data_check.main"
  runtime       = "python3.10"

}
resource "aws_s3_bucket" "bucket1" {
  bucket = "s3tempstorage17628a"
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_check.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket1.arn
}
resource "aws_s3_bucket_notification" "s3_update_notification" {
  bucket = aws_s3_bucket.bucket1.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.data_check.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".log"
  }
  depends_on = [aws_lambda_permission.allow_bucket]
}
