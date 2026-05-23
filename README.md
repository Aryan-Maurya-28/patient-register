# Patient Register 🏥

A comprehensive patient management system built with **Python**. Efficiently manage patient records, medical history, appointments, and healthcare information with an intuitive and secure interface.

## 🎯 Features

- **Patient Registration** - Easy and detailed patient enrollment
- **Medical History** - Complete patient health records and medical history
- **Appointment Management** - Schedule and track patient appointments
- **Search & Filter** - Quick access to patient records with powerful search
- **Data Validation** - Ensure accurate and consistent patient information
- **Secure Storage** - Protected patient data with proper access controls
- **Report Generation** - Generate detailed patient and health reports
- **User-Friendly Interface** - Clean CLI/GUI for easy navigation
- **Data Export** - Export patient records in multiple formats

## 📋 Key Components

- **Patient Database** - Centralized repository for all patient information
- **Appointment System** - Schedule management and reminders
- **Medical Records** - Comprehensive health history and treatment logs
- **Search Module** - Fast and flexible patient lookup
- **Reporting Tools** - Generate insights and statistics

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Aryan-Maurya-28/patient-register.git
   cd patient-register
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

## 📖 Usage Guide

### Register a New Patient

```python
# Access the patient registration module
- Select "Register Patient" from main menu
- Enter patient details (name, DOB, contact, etc.)
- Add medical history and allergies
- Confirm and save
```

### View Patient Records

```python
# Search for patient records
- Use search functionality by patient ID or name
- View complete medical history
- Check scheduled appointments
- Update patient information
```

### Schedule Appointments

```python
# Manage appointments
- Select appointment scheduling option
- Choose patient
- Set date, time, and reason
- Confirm appointment
```

### Generate Reports

```python
# Create reports
- Select report type (patient summary, appointment list, etc.)
- Choose date range if applicable
- Export in desired format (PDF, CSV, Excel)
```

## 🛠️ Technical Stack

- **Language**: Python 3.8+
- **Database**: [SQLite/MySQL/PostgreSQL - specify your choice]
- **CLI/GUI Framework**: [Tkinter/PyQt/Flask - specify your choice]
- **Data Handling**: pandas, numpy (if applicable)
- **File Format Support**: CSV, JSON, PDF (if applicable)
- **Package Manager**: pip

## 📁 Project Structure

```
patient-register/
├── src/
│   ├── main.py              # Application entry point
│   ├── patient.py           # Patient class and operations
│   ├── appointment.py       # Appointment management
│   ├── database.py          # Database operations
│   ├── utils.py             # Utility functions
│   ├── validators.py        # Data validation
│   └── reports.py           # Report generation
├── data/
│   ├── patients.db          # Patient database
│   └── appointments.db      # Appointment database
├── tests/
│   ├── test_patient.py
│   ├── test_appointment.py
│   └── test_database.py
├── requirements.txt         # Project dependencies
├── config.py               # Configuration settings
├── README.md               # This file
└── LICENSE                 # License information
```

## 📦 Dependencies

Core dependencies (see `requirements.txt` for complete list):

```
# Database
sqlalchemy>=1.4.0
# or
mysql-connector-python>=8.0.0

# Data Processing
pandas>=1.3.0
numpy>=1.21.0

# CLI Interface (if applicable)
click>=8.0.0

# GUI (if applicable)
PyQt5>=5.15.0
# or
tkinter

# Utilities
python-dateutil>=2.8.0
```

## 🔧 Configuration

1. **Edit `config.py` to customize settings:**
   ```python
   DATABASE_URL = 'sqlite:///patient_data.db'
   MAX_RECORDS_PER_PAGE = 20
   DATE_FORMAT = '%Y-%m-%d'
   ```

2. **Database Setup:**
   - Automatic on first run
   - Or manually run: `python setup_database.py`

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/
```

Run specific test file:
```bash
python -m pytest tests/test_patient.py -v
```

## 📊 Database Schema

### Patient Table
```
- patient_id (PRIMARY KEY)
- first_name
- last_name
- date_of_birth
- gender
- contact_number
- email
- address
- medical_history
- allergies
- created_at
- updated_at
```

### Appointment Table
```
- appointment_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- appointment_date
- appointment_time
- reason
- status
- notes
- created_at
```

## 🔐 Security Features

- **Data Validation** - Input validation for all patient data
- **Secure Storage** - Encrypted sensitive information
- **Access Control** - User authentication (if applicable)
- **Data Backup** - Regular backup mechanisms
- **Error Handling** - Comprehensive error management

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Aryan Maurya**
- GitHub: [@Aryan-Maurya-28](https://github.com/Aryan-Maurya-28)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💡 Future Enhancements

- [ ] Web interface using Flask/Django
- [ ] User authentication and role-based access
- [ ] Email/SMS notifications for appointments
- [ ] Prescription management system
- [ ] Billing and insurance integration
- [ ] Medical imaging storage
- [ ] Patient portal for self-service
- [ ] Analytics and statistics dashboard
- [ ] Mobile app integration
- [ ] Multi-language support
- [ ] Telemedicine features
- [ ] HIPAA compliance enhancements

## 🐛 Known Issues

[List any known issues or limitations here]

## ❓ FAQ

**Q: How is patient data stored?**
A: Patient data is stored securely in a database with proper validation and error handling.

**Q: Can I export patient records?**
A: Yes, records can be exported in CSV, JSON, and PDF formats.

**Q: Is this HIPAA compliant?**
A: Current version implements basic security. For production healthcare use, additional compliance measures may be needed.

**Q: Can multiple users access the system?**
A: Yes, with proper database configuration and authentication setup.

## 📞 Support & Issues

Found a bug or have questions?
- [Open an issue](https://github.com/Aryan-Maurya-28/patient-register/issues)
- Check existing issues for similar problems
- Provide detailed error messages and steps to reproduce

## ⭐ Support the Project

If you find this patient management system helpful, please consider giving it a star! Your support helps others discover the project.

---

**Manage Patient Care Efficiently! 🏥💙**
