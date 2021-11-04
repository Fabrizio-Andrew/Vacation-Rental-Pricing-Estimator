from flask import Flask, request, make_response, render_template
import json
from standardization import standardize, destandardizePrice
from linearmodel import coefs, bias
from percentile import calculatePercentile

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

        # Calculate the percentile of the price estimate from z-score
        percentile = calculatePercentile(estimatez)
       
        # Create the response object
        responsepayload = {
            'estimate': estimate,
            'percentile': percentile,
            'recommendations': []
        }
        if standardizeddata['host_resp_over_few_days'] == 1:
            responsepayload['recommendations'].append('response_time')

        response = make_response(responsepayload)

        print(response)
        return response

if __name__ == '__main__':
    app.run(debug=True)