from app import db, Portfolio  # Import your Flask app, SQLAlchemy instance, and Portfolio model

# Drop all existing tables and create new ones
db.drop_all()
db.create_all()

# Define projects data
projects_data = [
    {'title': 'Project 1', 'description': 'Description of project 1', 'image_url': 'https://via.placeholder.com/350x150'},
    {'title': 'Project 2', 'description': 'Description of project 2', 'image_url': 'https://via.placeholder.com/350x150'},
    {'title': 'Project 3', 'description': 'Description of project 3', 'image_url': 'https://via.placeholder.com/350x150'}
]

# Add projects to the database
for data in projects_data:
    project = Portfolio(title=data['title'], description=data['description'], image_url=data['image_url'])
    db.session.add(project)

# Commit changes to the database
db.session.commit()

# Optionally, print a success message
print('Projects added to the database successfully!')
