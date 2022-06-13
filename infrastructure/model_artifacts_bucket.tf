resource "aws_s3_bucket" "model_artifacts" {
  bucket = "ml-production-artifacts"

  tags = {
    Name        = "ML Production"
  }
}
