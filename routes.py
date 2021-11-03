from flask import Flask, request, render_template
import json
from standardization import standardize, destandardizePrice
from linearmodel import coefs, bias

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estimate', methods=['POST'])
def estimate():
    if request.method == 'POST':
        
        # Collect and standardize user data
        data = json.loads(request.get_data('body'))
        standardizeddata = standardize(data)

        # Find the dot product of standardized user data and regression model coefficients
        dotproduct = sum(standardizeddata[key] * coefs.get(key, 0) for key in standardizeddata)

        # add the bias
        estimatez = dotproduct + bias

        # destandardize the price
        estimate = destandardizePrice(estimatez)
        
        print(f'Price is: {estimate}')
        return str(estimate)

if __name__ == '__main__':
    app.run(debug=True)