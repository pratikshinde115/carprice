
from flask import Flask, render_template,request,flash,redirect
import pickle
import pandas as pd



cars= pickle.load(open('clean_dataset.pkl','rb'))
model= pickle.load(open('car_price.pkl','rb'))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ljadfnjbf'

@app.route("/" , methods = ['POST' , 'GET'])
def car():
       

    if request.method == 'POST':
        company=sorted(cars['company'].unique())
        car_models=sorted(cars['name'].unique())
        year=sorted(cars['year'].unique(),reverse=True)
        fuel_type=cars['fuel_type'].unique()

        
        company_selected = request.form['company']
        car_models_selected = request.form['car_model']
        fuel_type_selected = request.form['fuel_type']
        year_selected = int(request.form['year'])
        kilometres_selected = request.form['kilometres']
        if company_selected == "":
            flash('company not selected')
            redirect('car')

        else:


            kilometres_selected = int(request.form['kilometres'])

            predictions = model.predict(pd.DataFrame([[car_models_selected,company_selected,year_selected, kilometres_selected, fuel_type_selected]],columns=['name','company','year','kms_driven','fuel_type']))
            predictions=int(predictions)
            return render_template('car.html', company = company , car_model = car_models , year = year, fuel_type = fuel_type ,predictions = predictions)

    else :
        company=sorted(cars['company'].unique())
        car_models=sorted(cars['name'].unique())
        year=sorted(cars['year'].unique(),reverse=True)
        fuel_type=cars['fuel_type'].unique()
    return render_template('car.html', company = company , car_model = car_models , year = year, fuel_type = fuel_type)
if __name__=='__main__':
    app.run(debug=True)