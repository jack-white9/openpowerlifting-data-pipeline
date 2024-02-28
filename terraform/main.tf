provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_s3_bucket" "raw" {
  bucket = "openpowerlifting-data-raw"
}

resource "aws_s3_bucket_lifecycle_configuration" "bucket-config" {
  bucket = aws_s3_bucket.raw.id

  rule {
    id = "expire"

    expiration {
      days = 10
    }

    status = "Enabled"
  }
}

resource "aws_s3_bucket" "curated" {
  bucket = "openpowerlifting-data-curated"
}
