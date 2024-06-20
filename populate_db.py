from app import db, Portfolio


db.drop_all()
db.create_all()

project1 = Portfolio(title='Project 1', description='Description of project 1', image_url='https://via.placeholder.com/350x150')
project2 = Portfolio(title='Project 2', description='Description of project 2', image_url='https://via.placeholder.com/350x150')
project3 = Portfolio(title='Project 3', description='Description of project 3', image_url='https://via.placeholder.com/350x150')


db.session.add(project1)
db.session.add(project2)
db.session.add(project3)
db.session.commit()
