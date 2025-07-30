# 💰 Personal Finance Manager CLI App

A **Command-Line Interface (CLI)** based Personal Finance Manager built with Python. This project allows users to **track expenses**, **set budgets**, **generate reports**, and **back up financial data** — all through a clean and interactive terminal interface.

---

## 🚀 Features

- 🔐 **User Authentication**  
  - Secure registration and login.

- 💸 **Transaction Management**  
  - Add, view, edit, delete, and search transactions.

- 📊 **Budgeting System**  
  - Set monthly budgets with real-time warning alerts when overspending.

- 📈 **Reports & Insights**  
  - Generate detailed financial reports for better decision-making.

- 🗃️ **Data Backup & Restore**  
  - Create and restore backups of your financial data with a single click.

- 💻 **Clean Terminal Interface**  
  - User-friendly CLI menus for smooth navigation.

---

## 🧩 Project Structure

```
personal-finance-cli-app/
│
├── auth.py               # User registration and login system
├── backup.py             # Backup and restore logic
├── budget.py             # Budget operations and budget warnings
├── db_init.py            # Initializes database tables
├── report.py             # Generates financial reports
├── tracker.py            # CRUD operations for transactions
├── ui_utils.py           # CLI helpers (clear, banner, pause)
├── main.py               # Entry point and menu logic
└── finance.db            # SQLite database (auto-created)
```

---

## 🛠️ Getting Started

### ✅ Prerequisites

- Python 3.7 or above installed

### 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/personal-finance-cli-app.git
   cd personal-finance-cli-app
   ```

2. **Run the Application**
   ```bash
   python main.py
   ```

> Note: All necessary database tables will be initialized automatically.

---

## 💡 How It Works

1. Launch the program using `python main.py`.
2. Choose to **Register** or **Login**.
3. Once logged in, you'll see the **Dashboard** with:
   - Transactions & Budgets
   - Reports & Tools
   - Backup & Settings

4. You can:
   - Add, edit, delete, or search transactions
   - Set or view monthly budgets
   - Generate financial summaries
   - Back up or restore your data

---

## 📸 Sample CLI Flow

```bash
=== Personal Finance Manager ===
1. Register
2. Login
3. Exit

> 2
Login: ashutosh
Password: *****

=== Dashboard ===
1. Transactions & Budget
2. Reports & Tools
3. Backup & Settings
```

---

## 🔐 Security

- User-specific data isolation is maintained using unique IDs.
- You can implement password hashing (e.g., using `bcrypt`) for extra security.

---


## 🤝 Contributing

Want to improve this project?

1. Fork the repo
2. Create a branch (`feature/your-feature`)
3. Commit your changes
4. Push the branch
5. Open a Pull Request 🚀

---
## 👨‍💻 Author

**Ashutosh Dubey**  
Acropolis Institute of Technology and Research  
[LinkedIn](https://www.linkedin.com/in/ashutosh-dubey-dev/)

---

## 🙏 Acknowledgements

- Python Standard Libraries (`sqlite3`, `os`, `shutil`, etc.)
- CLI design inspired by real-world finance tools
