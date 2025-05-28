# Helpline Databse Definition

## Engine: `MongoDB`
## Libraries: `pymongo`

# Global System Data
The file `models/system.py`

# Case Management Data
The file `models/casedata/metadata.py`

# Call Management (CDR) Data
The file `models/calldata/metadata.py`

The file `models/calldata/runtime.py` tracks **Asterisk** calls using `Websockets` and `Asterisk REST API` **ARI**

# Quality Control Data
The file `models/qcondata/metadata.py`

# Access Control (Users) Data
The file `models/userdata/metadata.py` handles `user registration`, `login session`, and `access control`. Define Levels:
## supervisor
Elevated roles include `QA`
## counselor
## caseworker
## system admin
## guests
Include participation at call level for 3rd-party guests like volunteer counselors, legal and law enforcement who can be called upon to participate in `care plan`. This people will dial `116` when invited. The invite button is active for designated calls
