# 📄 Text File Converter

### 📝 Overview
The **Text File Converter** application monitors a specified input directory for `.txt` files, converts them to UTF-8 encoding, and saves the converted files in an output directory. Processed files are automatically moved to a separate `processed` folder inside the input directory to keep everything organized. Non-`.txt` files are moved to an `errors` folder.

---

## 🚀 Getting Started

### 📋 Prerequisites
- Docker
- Python 3.10+
- `make` (optional, for easier building and running)

---

### ⚙️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/text-file-converter.git
   cd text-file-converter

### **Prepare Environment Variables**

1. **Create a `.env` file** in the root directory with the following variables:

   ```plaintext
   INPUT_DIRECTORY=./input_files
   OUTPUT_DIRECTORY=./output_files
   MAX_WORKERS=2

2. **Ensure that the input_files and output_files directories are created:**

   ```bash
    mkdir -p input_files output_files
   
3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt


## 🐳 Using Docker

The project includes a Dockerfile and Makefile to facilitate building and running the containerized application.

### Building the Docker Image

Build the Docker image using the following command:
```bash
make build
```

This command will create an image named text_file_converter.


### Running the Docker Container

Run the application in a Docker container with mapped input and output directories:
```bash
make run
```
The make run command will:

- Remove any existing container named text_file_converter_container.
- Run a new container named text_file_converter_container with mapped directories:
- input_files in your current directory will be accessible as /app/input_files in the container.
- output_files in your current directory will be accessible as /app/output_files in the container.

### Cleaning Up
To remove both the container and the image, use:
```bash
make clean
```

## 🛠️ How It Works
### File Monitoring: 
The application monitors the specified input_files directory for new .txt files.
### Conversion: 
Each .txt file is converted to UTF-8 encoding and saved in the output_files directory with _utf8_converted added to the filename.
### File Organization:
After conversion, the original file is moved to the processed folder inside input_files.
Files that are not .txt are moved to an errors folder inside input_files.

## 🔍 Additional Notes
### Logging: 
Logs are saved in a file named conversion.log in the root directory. It records all debug and error information.
### Customizing:
Modify MAX_WORKERS in .env to set the number of files processed simultaneously.

## 🤖 Running Locally Without Docker
To run the application locally:

```bash
python main.py
```

Ensure that the environment variables in .env are properly configured and requirements are installed before running locally.

## 🎉 You're All Set!
You are now ready to use Text File Converter. Just add .txt files to the input_files directory, and they’ll automatically be converted and organized. Files that are not .txt will be moved to the errors folder.