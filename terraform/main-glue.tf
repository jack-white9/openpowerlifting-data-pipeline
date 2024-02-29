# Create database & crawler

resource "aws_glue_catalog_database" "this" {
  name = "openpowerlifting-database"
}

resource "aws_glue_crawler" "this" {
  database_name = aws_glue_catalog_database.this.name
  name          = "openpowerlifting-crawler"
  role          = aws_iam_role.this.arn

  s3_target {
    path = "s3://${aws_s3_bucket.curated.bucket}/"
  }
}

# Create IAM policies and roles

data "aws_iam_policy_document" "assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "access" {
  statement {
    effect    = "Allow"
    actions   = ["logs:*"]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["cloudwatch:*"]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["glue:*"]
    resources = ["*"]
  }
}

resource "aws_iam_role" "this" {
  name                  = "openpowerlifting-glue-crawler-execution-role"
  assume_role_policy    = data.aws_iam_policy_document.assume.json
  description           = "IAM execution role for OpenPowerlifting Glue Crawler"
  force_detach_policies = true
}

resource "aws_iam_policy" "access" {
  name        = "openpowerlifting-glue-crawler-access-policy"
  description = "Policy for MWAA to access CloudWatch, S3, SQS and KMS"
  policy      = data.aws_iam_policy_document.access.json
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.access.arn
}
