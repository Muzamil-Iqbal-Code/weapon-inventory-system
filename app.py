from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Flask app setup
app = Flask(__name__)
app.secret_key = "supersecret123"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weapons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Weapon model
class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Available, Maintenance, Decommissioned

    def __repr__(self):
        return f"<Weapon {self.name}>"

# Create DB tables
with app.app_context():
    db.create_all()

# Home route -> redirect to weapons list
@app.route('/')
def home():
    return redirect(url_for('show_weapons'))

# View all weapons
@app.route('/weapons')
def show_weapons():
    weapons = Weapon.query.all()
    return render_template('weapons.html', weapons=weapons)

# Add new weapon
@app.route('/add', methods=['GET', 'POST'])
def add_weapon():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        manufacturer = request.form['manufacturer']
        year = request.form['year']
        status = request.form['status']

        # Validation
        if not name or not type_ or not manufacturer or not year or not status:
            flash("All fields are required!", "error")
            return redirect(url_for('add_weapon'))
        if not year.isdigit() or int(year) < 1800 or int(year) > 2030:
            flash("Year must be a valid number between 1800 and 2030!", "error")
            return redirect(url_for('add_weapon'))

        new_weapon = Weapon(
            name=name,
            type=type_,
            manufacturer=manufacturer,
            year=int(year),
            status=status
        )
        db.session.add(new_weapon)
        db.session.commit()
        flash("Weapon added successfully!")
        return redirect(url_for('show_weapons'))

    return render_template('add_weapon.html')

# Edit weapon
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_weapon(id):
    weapon = Weapon.query.get_or_404(id)

    if request.method == 'POST':
        weapon.name = request.form['name']
        weapon.type = request.form['type']
        weapon.manufacturer = request.form['manufacturer']
        weapon.year = int(request.form['year'])
        weapon.status = request.form['status']

        db.session.commit()
        flash("Weapon updated successfully!")
        return redirect(url_for('show_weapons'))

    return render_template('edit_weapon.html', weapon=weapon)

# Delete weapon
@app.route('/delete/<int:id>', methods=['POST'])
def delete_weapon(id):
    weapon = Weapon.query.get_or_404(id)
    db.session.delete(weapon)
    db.session.commit()
    flash("Weapon deleted successfully!")
    return redirect(url_for('show_weapons'))

# Run app
if __name__ == '__main__':
    app.run(debug=True)
