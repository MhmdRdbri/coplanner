# Coplanner

Coplanner is a web-based project management application designed to enhance team collaboration and streamline project workflows. It offers features such as task scheduling, resource allocation, and real-time progress tracking to ensure efficient project execution.

## Table of Contents

  - [Features](#features)
  - [Built With](#built-With)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

### Features

* **Task Scheduling**: Plan and assign tasks with deadlines to ensure timely project completion.
* **Resource Allocation**: Manage resources effectively by allocating them to tasks based on availability and priority.
* **Task Management:** Assign, track, and prioritize tasks to ensure critical activities are completed on schedule.
* **Real-Time Progress Tracking**: Monitor project progress with up-to-date dashboards and notifications.
* **Team Collaboration**: Facilitate seamless communication among team members through integrated messaging and file-sharing options.
* **Meeting Management**: Ability to set meeting time and announce to members
* **Work Report**: The employees of the company send their daily work reports to the relevant officials and the officials can confirm them if they check
* **Telegram Bot**: A special Telegram bot for this crm where people can see news and website changes notification in their chat.

# Built With
* **Backend:** Python(Django)
* **API Development:** RESTful APIs
* **Database:** PostgreSQL, redis
* **Authentication:** JWT Token, Role-Based Access Control
* **Caching & Performance Optimization:** Redis, Celery
* **Version Control & Collaboration:** Git, GitHub
* **Task Scheduling & Automation:** Celery, Cron Jobs
* **Telegram Bot:** telegram.ext Library


# Getting Started

Follow these instructions to set up and run the Sales-CRM system locally.

## Installation

1. **Clone the Repository:**

```bash
git clone https://github.com/MhmdRdbri/coplanner.git
cd coplanner
```

2. **Set Up the Virtual Environment:**

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
Then, install the required packages:

```bash
pip install -r requirements.txt
```

Set Up Environment Variables:
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/coplanner
```

Apply Migrations:
```bash
python manage.py migrate
```

## Usage

1. **Start the Backend Server:**
```bash
python manage.py runserver
```
2. Access the Admin Panel:
   - Open your browser and navigate to http://localhost:8000/admin to manage the CRM data.

## Contributing

Contributions are welcome! Please follow these steps:
* **Fork the Repository:** Click the "Fork" button at the top right corner of this repository.
* **Clone Your Fork:** Clone your forked repository to your local machine.
* **Create a New Branch:** Use git checkout -b your-feature-branch to create a new branch.
* **Make Changes:** Implement your feature or fix.
* **Commit Changes:** Use git commit -m 'Add new feature' to commit your changes.
* **Push to Fork:** Push your changes to your forked repository.
* **Open a Pull Request:** Navigate to the original repository and click "New Pull Request".

## License

This project is licensed under the MIT License. See the LICENSE file for details.
