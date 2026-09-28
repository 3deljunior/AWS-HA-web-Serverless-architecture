import os
import boto3
import psycopg2
from flask import Flask, request, render_template

app = Flask(__name__)

# Environment configurations for S3 and RDS
S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT', '5432')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# Initialize the S3 client (Credentials are inherited from the EC2 IAM Role)
s3 = boto3.client('s3', region_name=AWS_REGION)

def get_db_connection():
    """Establish and return a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        image_file = request.files.get('image')

        # Input validation
        if not name or not image_file or image_file.filename == '':
            return render_template('index.html', message="Please fill in all fields and select an image.", success=False)

        try:
            # 1. Upload the image to the S3 Bucket
            filename = image_file.filename
            s3.upload_fileobj(image_file, S3_BUCKET, filename)
            
            # Construct the public S3 URL (assuming the bucket allows public read or you generate pre-signed URLs later)
            image_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

            # 2. Save the text data and image URL to the RDS PostgreSQL database
            conn = get_db_connection()
            cur = conn.cursor()
            
            insert_query = "INSERT INTO users (name, image_url) VALUES (%s, %s);"
            cur.execute(insert_query, (name, image_url))
            
            conn.commit()
            cur.close()
            conn.close()

            return render_template('index.html', message="Data and image saved successfully!", success=True)
            
        except Exception as e:
            return render_template('index.html', message=f"An error occurred: {str(e)}", success=False)

    # Render the initial form on GET request
    return render_template('index.html')

if __name__ == '__main__':
    # Listen on all available IPs on port 80
    app.run(host='0.0.0.0', port=80)
