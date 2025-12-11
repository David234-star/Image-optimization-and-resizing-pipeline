# Serverless Image Optimization Pipeline on AWS

A fully serverless architecture that automatically resizes and optimizes images uploaded by users. This project leverages AWS Lambda, S3, and API Gateway to create an event-driven image processing pipeline suitable for portfolios, CMS, or e-commerce applications.

## 🚀 Overview

This application allows users to upload high-resolution images via a web frontend. The system automatically:

1. Securely uploads the file to an S3 bucket (using Pre-signed URLs).
2. Triggers a Python Lambda function.
3. Resizes the image to standard web resolutions (1080p, 720p, Mobile).
4. Converts the image to **WebP format** for optimized web performance.
5. Saves the processed images to a public destination bucket.

## 🏗 Architecture

**User** → **Frontend (S3)** → **API Gateway** → **Lambda (Auth)** → **S3 Source Bucket** ⚡ (Trigger) → **Lambda (Processor)** → **S3 Dest Bucket**

1. **Frontend:** Static HTML/JS hosted on S3.
2. **API Gateway:** Exposes an endpoint to generate secure upload links.
3. **Lambda (GetUploadURL):** Generates a short-lived S3 Pre-signed URL.
4. **S3 Source:** Stores the raw, original upload.
5. **Lambda (ImageOptimizer):** Uses the **Pillow** library to resize and compress.
6. **S3 Destination:** Stores the final optimized assets.

## 🛠 Tech Stack

- **Cloud Provider:** Amazon Web Services (AWS)
- **Infrastructure:**
  - **Compute:** AWS Lambda (Python 3.10)
  - **Storage:** Amazon S3 (Source, Destination, Frontend Hosting)
  - **API:** AWS API Gateway (HTTP API)
- **Libraries:**
  - **Python:** `boto3` (AWS SDK), `Pillow` (Image Processing)
  - **Frontend:** Pure HTML5 / JavaScript (ES6)

## 📂 Project Structure

```text
Image-optimization-and-resizing-pipeline/
│
├── frontend/
│   └── index.html             # The User Interface (HTML + JS)
│
├── lambda/
│   ├── get-upload-url/
│   │   └── lambda_function.py # Python code for API Gateway Auth
│   │
│   └── image-processing/
│       └── lambda_function.py # Python code using Pillow (Resize logic)
│
└── README.md                  # Documentation file
```

## ⚙️ Setup & Deployment

### 1. S3 Buckets

Create three buckets:

- `source-bucket`: Private, CORS enabled (Block Public Access: ON).
- `dest-bucket`: Public Read access (Block Public Access: OFF).
- `frontend-bucket`: Static Website Hosting enabled.

### 2. IAM Role

Create a role `ImageProcessingRole` with permissions:

- `AWSLambdaBasicExecutionRole`
- `AmazonS3FullAccess`

### 3. Lambda Functions

**Function A: GetUploadURL**

- **Runtime:** Python 3.10
- **Env:** Set `BUCKET_NAME` to your source bucket.
- **Region Config:** Ensure `boto3` config specifies the correct region (e.g., `us-east-2`) to avoid CORS redirects.

**Function B: ImageOptimizer**

- **Runtime:** Python 3.10
- **Layer:** Add the **Klayers Pillow** ARN for your region.
- **Trigger:** S3 Event Notification (All object create events) on the Source Bucket.

### 4. API Gateway

- Create an HTTP API.
- Integration: Connect to `GetUploadURL` Lambda.
- **CORS:** Enable CORS with `Access-Control-Allow-Origin: *`.

## 🧪 Optimization Results

| Metric         | Original Image (JPEG) | Optimized Image (WebP) |
| :------------- | :-------------------- | :--------------------- |
| **Resolution** | 4000x3000 (12MP)      | 1920x1440 (1080p)      |
| **File Size**  | ~4.5 MB               | **~150 KB**            |
| **Reduction**  | -                     | **~96%**               |

## 📝 Key Learnings & Configuration

- **S3 CORS:** Crucial for allowing browser-based uploads to private buckets.
- **Lambda Layers:** Python's Pillow library must be added as a layer since it includes compiled C binaries.
- **Region Locking:** When generating pre-signed URLs in newer AWS regions (like `us-east-2`), the region must be explicitly defined in the `boto3` client config.

## 📄 License

This project is open-source and available under the MIT License.

```

```
