# ltr-lambda-helpers

This repository contains [AWS Lambda](https://aws.amazon.com/lambda/) functions to retrieve and store public data from Canadian government websites.

## lambda-download-to-s3.py

This function retrieves the specified webpage or online file, downloads it temporarily, and then sends it to a specified S3 bucket.

It requires the following 4 environment variables to be set:

* `url`: the webpage or online file to be downloaded
* `destination_bucket`: an S3 bucket that the Lambda function is able to write to
* `destination_folder`: a subfolder within that S3 bucket (created automatically if it doesn't already exist)
* `destination_file`: the destination file within that subfolder, in the S3 bucket (this can be the same as the original online filename)

For example, for downloading [completed Access to Information summaries](https://open.canada.ca/data/en/dataset/0797e893-751e-4695-8229-a5066e4fe43c), the following 4 environment variables are used:

* `url`: `https://open.canada.ca/data/dataset/0797e893-751e-4695-8229-a5066e4fe43c/resource/19383ca2-b01a-487d-88f7-e1ffbc7d39c2/download/ati.csv`
* `destination_bucket`: `ltr-archive-ati-summaries` (your own AWS instance must have a matching S3 bucket name)
* `destination_folder`: `ati-summaries`
* `destination_file`: `ati.csv`

Ensure that you have IAM permissions set for the Lambda function role that allow it to write to S3 buckets (this is not the case by default). 

To ensure the script has time to download and upload the CSV file, increase the Lambda maximum execution time to at least 10 seconds.

Inspired by the [ATI Review – Interim What We Heard Report](https://www.canada.ca/en/treasury-board-secretariat/services/access-information-privacy/reviewing-access-information/the-review-process/ati-review-interim-what-we-heard-report.html#toc2-2).

As always, [feedback](https://twitter.com/sboots) and [issue requests](https://github.com/ltr-archive/ltr-lambda-helpers/issues) welcome!
