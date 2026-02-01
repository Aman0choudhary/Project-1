# Project-1

Image Steganography Flask App

A simple Flask-based web application that allows users to hide (encode) and reveal (decode) secret messages inside images using steganography techniques.

Built with Python, Flask, and Pillow.

##🚀 Features

Encode secret text inside an image

Decode hidden text from an image

Supports PNG / JPG / JPEG images

Simple web interface

Secure environment variable handling with .env

Lightweight and beginner-friendly project

##🛠️ Tech Stack

Backend: Flask 2.2.2

Image Processing: Pillow

Steganography: steganocryptopy

Environment Management: python-dotenv

HTTP Requests: requests

Server Utilities: werkzeug

## 📂 Project Structure
```
project/
│── app.py
│── debug_test.py
│── requirements.txt
│── README.md
│── .gitignore
│── templates/
│   └── index.html
│── uploads/
│   ├── original_image.png
│   └── encoded_image.png
```
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/Project-1.git
cd Project-1

2️⃣ Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Create .env file
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key

5️⃣ Run the app
python app.py


Open browser:

http://127.0.0.1:5000

##🧪 Example Use Case

-Upload an image
-Enter a secret message
-Download encoded image
-Upload encoded image to decode the hidden message

##📌 Future Improvements

-User authentication
-Drag-and-drop upload UI
-Download history
-Deployment on Render / Railway / Vercel
-Better UI with Tailwind or Bootstrap

🤝 Contributing

Pull requests are welcome!
Feel free to fork this repo and improve it.

⭐ Support

If you like this project, give it a ⭐ on GitHub — it motivates a lot 😄

##👨‍💻 Author

Aman Tetarwal

Student | Python | Flask | Learning Full-Stack Development