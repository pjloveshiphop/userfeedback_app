from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app=Flask(__name__)

ENV = 'prod'

if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:wkrlfur3@localhost/Hyundai'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://kwcbowqywgbrqd:c08de26eecb81231fc7627fb0ddc3964ce2b4747098c52597a92ce4af56ce942@ec2-34-199-149-157.compute-1.amazonaws.com:5432/d861fnaul76nud'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

#create db model
class Feedback(db.Model):
    __tablename__='feedback'
    id=db.Column(db.Integer, primary_key=True)
    customer=db.Column(db.String(200), unique=True)
    dealer=db.Column(db.String(200))
    rating=db.Column(db.Integer)
    comments=db.Column(db.Text())
    useremail=db.Column(db.String(200))

    def __init__(self, customer, dealer, rating, comments, useremail):
        self.customer=customer
        self.dealer=dealer
        self.rating=rating
        self.comments=comments
        self.useremail=useremail 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method=='POST':
        customer=request.form['customer']
        dealer=request.form['dealer']
        rating=request.form['rating']
        comments=request.form['comments']
        useremail=request.form['useremail']
        #print(customer, dealer, rating, comments, useremail)
        if customer=='' or dealer=='':
            return render_template('index.html', message="Please enter required fields")
        
        #prevent a user keep submitting feedback over again and again
        if db.session.query(Feedback).filter(Feedback.customer==customer).count()==0:
            data=Feedback(customer,dealer,rating,comments,useremail)
            db.session.add(data)
            db.session.commit()

            #send email after db commits
            send_mail(customer, dealer, rating, comments, useremail)

            return render_template('success.html')
        return render_template('index.html', message="You've submitted feedback")

if __name__ == '__main__':
    
    app.run()


