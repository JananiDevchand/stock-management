A simple web app to manage stock inventory using Flask and MongoDB.

⚙️ Features
Admin login/authentication

Add, update, delete stock items

Search & filter by quantity and price

Inventory charts (Chart.js)

Pure CSS styling (no Bootstrap)

🚀 Getting Started
1. Clone & Install
bash
Copy
Edit
git clone https://github.com/yourusername/stock-management.git
cd stock-management
pip install -r requirements.txt
2. Start MongoDB
bash
Copy
Edit
mongod
3. Create Admin User
bash
Copy
Edit
python create_admin.py
4. Run App
bash
Copy
Edit
python app.py
Visit: http://localhost:5000

👤 Default Admin
Username: admin

Password: set in create_admin.py

📁 Project Structure
cpp
Copy
Edit
app.py
create_admin.py
templates/
static/