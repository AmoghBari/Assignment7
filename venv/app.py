from flask import Flask, render_template, request, flash
import boto3
from decouple import config
from prometheus_client import Counter, Gauge, generate_latest, REGISTRY
from prometheus_client.exposition import MetricsHandler
import psutil


app = Flask(__name__)


#  ----------------  AWS S3 Configurations  ----------------


AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_REGION = config('AWS_REGION')



#  ----------------  Boto3 Configuration  ----------------


s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
    region_name=AWS_REGION
)
request_counter = Counter('flask_requests', 'Total Requests Received')
cpu_usage = Gauge('flask_cpu', 'CPU Usage')

@app.route('/metrics')
def metrics():
    cpu_percentage = psutil.cpu_percent()
    cpu_usage.set(cpu_percentage)

    return generate_latest(REGISTRY)



#  ----------------  HOMEPAGE  ----------------


@app.route('/')
def index():
    request_counter.inc()
    return render_template('index.html')



#  ----------------  Creating S3 Bucket  ----------------


@app.route('/create_bucket', methods=['POST'])

def create_bucket():
    bucket_name = request.form.get('bucket_name')


    #  ----------  Create Bucket  ----------

    try:
        s3.create_bucket(Bucket = bucket_name)
    except Exception as e:
        flash(f'Error Creating S3 Bucket: {str(e)}', "Unsuccessful")
    flash(f'S3 Bucket "{bucket_name}" created successfully!')
    return render_template('index.html')



#  ----------------  Listing S3 Buckets  ----------------


@app.route('/list_buckets')

def list_buckets():


    #  ----------  List Bucket  ----------

    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return render_template('index.html', buckets=buckets)



#  ----------------  Deleting S3 Bucket  ----------------


@app.route('/delete_bucket', methods=['POST', 'GET'])

def delete_bucket():
    if request.method == 'POST':
        bucket_name = request.form['bucket_name']


        #  ----------  Delete Bucket  ----------

        try:
            s3.delete_bucket(Bucket=bucket_name)
            flash(f"Bucket {bucket_name} Deleted Successfully")
        except Exception as e:
            flash(f"An Error Occurred: {str(e)}")
    return render_template('index.html')



#  ----------------  Uploading File To S3 Bucket  ----------------


@app.route('/upload_file', methods=['POST'])

def upload_file():
    bucket_name = request.form.get('bucket_name')
    file = request.files['file']


    #  ----------  Upload File  ----------

    try:
        filename = file.filename
        s3.upload_fileobj(file,bucket_name,filename)
        flash(f"File Uploaded Successfully to {bucket_name}")
    except Exception as e:
        flash(f"An Error Occurred: {str(e)}")
    return render_template('index.html')



#  ----------------  Listing Objects in S3 Buckets  ----------------


@app.route('/list_objects', methods=['POST'])

def list_objects():
    objects = []
    bucket_name = request.form.get('bucket_name')


    #  ----------  List Objects  ----------

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        for obj in response['Contents']:
            objects.append(obj['Key'])
    except Exception as e:
        flash(f"{bucket_name} Bucket Is Empty")
    return render_template('index.html', objects=objects)



#  ----------------  Deleting File From S3 Bucket  ----------------


@app.route('/delete_files', methods=['POST'])

def delete_objects():
    bucket_name = request.form.get('bucket_name')
    object_key = request.form.get('object_key')


    #  ----------  Delete File  ----------

    try:
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        flash(f"Successfully Deleted Object' {object_key}' from {bucket_name}")
    except Exception as e:
        flash(f"Error Deleting Object: '{str(e)}'")
    return render_template('index.html')



#  ----------------  Copying File Within S3 Buckets  ----------------


@app.route('/copy_files', methods = ['POST'])

def copy_file():
    source_bucket = request.form.get('source_bucket')
    destination_bucket = request.form.get('destination_bucket')
    source_key = request.form.get('source_key')
    destination_key = request.form.get('destination_key')


    #  ----------  Copy File  ----------

    try:
        s3.copy_object(CopySource=f'{source_bucket}/{source_key}', Bucket=destination_bucket, Key=destination_key)
        flash(f'Successfully Copied File From {source_bucket}/{source_key} to {destination_bucket}/{destination_key}')
    except Exception as e:
        flash(f'Error Copying File: {str(e)}')
    return render_template('index.html')



#  ----------------  Moving File Withing S3 Buckets  ----------------


@app.route('/move_files', methods=['POST'])

def move_file():
    source_bucket = request.form.get('source_bucket')
    destination_bucket = request.form.get('destination_bucket')
    file_key = request.form.get('file_key')
    source_key = request.form.get('source_key')
    destination_key = request.form.get('destination_key')


    #  ----------  Move File  ----------

    try:
        s3.copy_object(CopySource={'Bucket':source_bucket, 'Key':file_key},
                       Bucket=destination_bucket, Key=file_key)
        s3.delete_object(Bucket=source_bucket, Key=file_key)
        flash(f'Successfully Moved File From {source_bucket}/{source_key} to {destination_bucket}/{destination_key}')
    except Exception as e:
        flash(f"Error Moving File: {e}")
    return render_template('index.html')



#  ----------------  Creating Folder In S3 Bucket  ----------------


@app.route('/create_folder', methods=['POST'])

def create_folder():
    bucket_name = request.form.get('bucket_name')
    folder_name = request.form.get('folder_name')


    #  ----------  Create Folder  ----------

    if folder_name:
        if not folder_name.endswith('/'):
            folder_name += '/'

        s3.put_object(Bucket=bucket_name, Key=folder_name)
        flash(f"Folder '{folder_name}' Created Successfully in Bucket {bucket_name}")
    else:
        flash("Folder Name Cannot Be Empty.")
    return render_template('index.html')



#  ----------------  Deleting Folder From S3 Bucket  ----------------


@app.route('/delete_folder', methods=['POST'])

def delete_folder():
    folder_name = request.form.get('folder_name')
    bucket_name = request.form.get('bucket_name')


    #  ----------  Delete Folder  ----------

    objects_to_delete = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    if 'Contents' in objects_to_delete:
        for obj in objects_to_delete['Contents']:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
    flash(f" Folder {folder_name} Deleted Successfully From Bucket {bucket_name}")
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = config('AWS_SECRET_ACCESS_KEY')
    app.run(host = '0.0.0.0')