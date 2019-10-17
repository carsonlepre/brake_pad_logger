from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pads.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pads.db'
db = SQLAlchemy(app)

class Log(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, nullable=False)
    date_logged = db.Column(db.DateTime, nullable=False, default=datetime.now)
    front_pads = db.Column(db.String(15), nullable=False)
    rear_pads = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Log %r>' % self.vehicle_id

# Flask HTTP Server routes form submit post and form display here
@app.route('/', methods=['GET'])
def index():
    # Show default HTML form for creating break pad inspection
    return render_template('update.html')

def validate_vehicle_id(vehicle_id):
    validated_vehicle_id = -1
    # This will throw exception if string input is provided
    if int(vehicle_id) > 449:
        validated_vehicle_id = vehicle_id    
    return int(validated_vehicle_id)

@app.route('/update', methods=['POST', 'GET'])
def update():
    # HTTP method 'POST' wants to create a break pad inspection.
    if request.method == 'POST':
        try:
            # Read HTML form fields from user - TODO: validate this data
            vehicle_id = validate_vehicle_id(request.form['vehicle_id'])
            # Validate vehicle ID range 
            if vehicle_id < 0:
                return render_template('error-update.html')
            front_pad_data = request.form['front_pads']
            rear_pad_data = request.form['rear_pads']

            # Instantiate Log object from HTML form field data
            update = Log(vehicle_id=vehicle_id, front_pads=front_pad_data, rear_pads=rear_pad_data)
        
            # Generate SQL INSERT statement based on new Log object
            db.session.add(update)
            # Execute SQL statement
            db.session.commit()
            # Redirect user to update page 
            return redirect('/')
            
        # DB or Redirect Error- fix data!
        except:
            return render_template('error.html')
    else:
        return render_template('update.html')


if __name__ == "__main__":
    app.run(debug=True)